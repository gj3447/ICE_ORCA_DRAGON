// Rigorous C1 action-augmented flow backend for a bounded principal-branch runner.
// No files are written. Inputs are exact binary64 hexadecimal endpoints.
#include "capd/capdlib.h"
#include <cerrno>
#include <cfenv>
#include <cmath>
#include <cstdlib>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

using namespace capd;

// State order is (a,u,phi,v,T,I), with s=tau/T and I(0)=0.
const std::string FIELD =
    "par:b,p;var:a,u,phi,v,T,I;fun:"
    "T*u,"
    "T*((1-u^2)/(2*a)-a*v^2/4-3*a*(1-exp(-b*phi))^2/8),"
    "T*v,"
    "T*(3*b*exp(-b*phi)*(1-exp(-b*phi))/2-3*u*v/a),"
    "0,"
    "T*2*p^2*(-3*a*u^2+a^3*v^2/2-3*a+3*a^3*(1-exp(-b*phi))^2/4);";

const std::string FREE_FIELD =
    "var:a,u,phi,v,T,I;fun:T*u,0,T*v,0,0,T*(u^2+v^2)/2;";

std::string hex(double x) {
    if (!std::isfinite(x)) throw std::runtime_error("nonfinite interval endpoint");
    std::ostringstream out;
    out << std::hexfloat << x;
    return out.str();
}

std::string encoded(const interval& x) {
    return "{\"lower_hex\":\"" + hex(x.leftBound()) +
           "\",\"upper_hex\":\"" + hex(x.rightBound()) + "\"}";
}

std::string encoded(const IVector& x) {
    std::string out = "[";
    for (int i = 0; i < x.dimension(); ++i) {
        if (i) out += ",";
        out += encoded(x[i]);
    }
    return out + "]";
}

std::string encoded(const IMatrix& x) {
    std::string out = "[";
    for (int i = 0; i < x.numberOfRows(); ++i) {
        if (i) out += ",";
        out += "[";
        for (int j = 0; j < x.numberOfColumns(); ++j) {
            if (j) out += ",";
            out += encoded(x[i][j]);
        }
        out += "]";
    }
    return out + "]";
}

std::string quoted(const std::string& text) {
    std::string out = "\"";
    for (char c : text.substr(0, 2000)) {
        if (c == '"' || c == '\\') out += '\\';
        out += (c == '\n' || c == '\r' || c == '\t') ? ' ' : c;
    }
    return out + "\"";
}

double parse_hex_binary64(const char* text) {
    const std::string source(text);
    if (source.find_first_of("pP") == std::string::npos ||
        source.find("0x") == std::string::npos &&
        source.find("0X") == std::string::npos)
        throw std::runtime_error("expected binary64 hexadecimal endpoint");
    errno = 0;
    char* end = nullptr;
    const double value = std::strtod(text, &end);
    if (errno == ERANGE || end == text || *end != '\0' || !std::isfinite(value))
        throw std::runtime_error("invalid binary64 hexadecimal endpoint");
    return value;
}

interval input_interval(const char* lower, const char* upper) {
    const double lo = parse_hex_binary64(lower);
    const double hi = parse_hex_binary64(upper);
    if (lo > hi) throw std::runtime_error("reversed interval endpoints");
    // strtod under FE_TONEAREST recovers the exact binary64 input; CAPD then
    // imports each endpoint as a point interval.
    return interval(lo, hi);
}

struct Flow {
    IVector endpoint;
    IMatrix derivative;
    IVector tube;
    std::vector<interval> step_times;
};

Flow propagate(IMap& field, const IVector& initial, int order, int max_steps) {
    IOdeSolver solver(field, order);
    ITimeMap time_map(solver);
    time_map.stopAfterStep(true);
    C1HORect2Set state(initial);
    ITimeMap::SolutionCurve curve(interval(0));
    std::vector<interval> times;
    do {
        if (static_cast<int>(times.size()) >= max_steps)
            throw std::runtime_error("declared step cap reached");
        time_map(interval(1), state, curve);
        times.push_back(time_map.getCurrentTime());
    } while (!time_map.completed());
    // SolutionCurve interval evaluation hulls all overlapping validated pieces.
    return {IVector(state), IMatrix(state), curve(interval(0, 1)), times};
}

std::string encoded(const Flow& flow) {
    std::string times = "[";
    for (std::size_t i = 0; i < flow.step_times.size(); ++i) {
        if (i) times += ",";
        times += encoded(flow.step_times[i]);
    }
    return "{\"endpoint\":" + encoded(flow.endpoint) +
           ",\"derivative\":" + encoded(flow.derivative) +
           ",\"whole_time_tube\":" + encoded(flow.tube) +
           ",\"validated_steps\":" + std::to_string(flow.step_times.size()) +
           ",\"step_end_times\":" + times + "]}";
}

int main(int argc, char** argv) {
    try {
        const bool free_control = argc == 14 && std::string(argv[13]) == "--free-control";
        if (argc != 13 && !free_control)
            throw std::runtime_error(
                "expected 10 hexadecimal endpoints, order, maxsteps, and optional --free-control");
        std::fesetround(FE_TONEAREST);
        const interval a = input_interval(argv[1], argv[2]);
        const interval u = input_interval(argv[3], argv[4]);
        const interval phi = input_interval(argv[5], argv[6]);
        const interval v = input_interval(argv[7], argv[8]);
        const interval T = input_interval(argv[9], argv[10]);
        const int order = std::stoi(argv[11]);
        const int max_steps = std::stoi(argv[12]);
        if (order < 3 || order > 64 || max_steps < 1 || max_steps > 256)
            throw std::runtime_error("unsupported integration bounds");
        if (!(a.leftBound() > 0 && T.leftBound() > 0))
            throw std::runtime_error("nonpositive initial scale or duration");

        const IVector initial({a, u, phi, v, T, interval(0)});
        IMap field(free_control ? FREE_FIELD : FIELD);
        if (!free_control) {
            field.setParameter("b", sqrt(interval(2) / 3));
            // CAPD's interval pi() is an outward enclosure; it remains a
            // parameter so the parsed vector field contains no host pi literal.
            field.setParameter("p", interval::pi());
        }
        const IMatrix initial_jacobian = field.derivative(initial);
        const Flow flow = propagate(field, initial, order, max_steps);

        std::cout << "{\"status\":\"FLOW_ENCLOSURES_COMPUTED\","
            << "\"interval_format\":\"EXACT_BINARY64_HEX_ENDPOINTS\","
            << "\"mode\":" << quoted(free_control ? "free6state_control" : "starobinsky_action_augmented") << ","
            << "\"field\":" << quoted(free_control ? FREE_FIELD : FIELD) << ","
            << "\"initial\":" << encoded(initial) << ","
            << "\"initial_augmented_jacobian\":" << encoded(initial_jacobian) << ","
            << "\"flow\":" << encoded(flow) << "}\n";
        return 0;
    } catch (const std::exception& error) {
        std::cout << "{\"status\":\"INCONCLUSIVE_FLOW\",\"error\":" << quoted(error.what()) << "}\n";
        return 0;
    }
}
