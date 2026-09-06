// Rigorous C1 flow backend for the adjacent, bounded Python runner.
// No files are written. All interval endpoints are serialized as exact binary64 hex.
#include "capd/capdlib.h"
#include <cfenv>
#include <cmath>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

using namespace capd;

const std::string FIELD =
    "par:b;var:a,u,phi,v,T;fun:T*u,"
    "T*((1-u^2)/(2*a)-a*v^2/4-3*a*(1-exp(-b*phi))^2/8),"
    "T*v,T*(3*b*exp(-b*phi)*(1-exp(-b*phi))/2-3*u*v/a),0;";

// Integer digit operations and division enclose the exact decimal, including
// numerators larger than 2^53. No decimal boundary is silently rounded to a point.
interval decimal(const std::string& text) {
    interval value(0), denominator(1);
    bool fraction = false, negative = false;
    for (std::size_t i = 0; i < text.size(); ++i) {
        const char c = text[i];
        if (i == 0 && c == '-') { negative = true; continue; }
        if (c == '.' && !fraction) { fraction = true; continue; }
        if (c < '0' || c > '9') throw std::runtime_error("invalid exact decimal");
        value = value * 10 + (c - '0');
        if (fraction) denominator *= 10;
    }
    return (negative ? -value : value) / denominator;
}

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
    // Checking only the endpoints would not prove domain validity between steps.
    return {IVector(state), IMatrix(state), curve(interval(0,1)), times};
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
        ",\"step_end_times\":" + times + "]}";
}

std::string quoted(const std::string& text) {
    std::string out = "\"";
    for (char c : text.substr(0, 2000)) {
        if (c == '"' || c == '\\') out += '\\';
        out += (c == '\n' || c == '\r' || c == '\t') ? ' ' : c;
    }
    return out + "\"";
}

int main(int argc, char** argv) {
    try {
        if (argc != 11) throw std::runtime_error("expected 10 pinned input arguments");
        const interval boundary_a = decimal(argv[1]), boundary_phi = decimal(argv[2]);
        // A seed defines a chosen dyadic centre, not an exact physical datum.
        std::fesetround(FE_TONEAREST);
        const double u0 = std::stod(argv[3]), v0 = std::stod(argv[4]), t0 = std::stod(argv[5]);
        const double ru = std::ldexp(1., std::stoi(argv[6]));
        const double rv = std::ldexp(1., std::stoi(argv[7]));
        const double rt = std::ldexp(1., std::stoi(argv[8]));
        const int order = std::stoi(argv[9]), max_steps = std::stoi(argv[10]);
        if (order < 3 || order > 64 || max_steps < 1 || max_steps > 256)
            throw std::runtime_error("unsupported integration bounds");
        IVector centre({interval(u0), interval(v0), interval(t0)});
        IVector radii({interval(ru), interval(rv), interval(rt)});
        IVector box(3);
        for (int i = 0; i < 3; ++i) box[i] = centre[i] + interval(-1,1)*radii[i];
        if (!(boundary_a.leftBound() > 0 && box[2].leftBound() > 0))
            throw std::runtime_error("nonpositive initial scale or duration");
        IVector point({boundary_a, centre[0], boundary_phi, centre[1], centre[2]});
        IVector initial({boundary_a, box[0], boundary_phi, box[1], box[2]});
        IMap field(FIELD);
        field.setParameter("b", sqrt(interval(2)/3));
        const IMatrix initial_jacobian = field.derivative(point);
        const Flow point_flow = propagate(field, point, order, max_steps);
        const Flow box_flow = propagate(field, initial, order, max_steps);

        // Exactly solvable dyadic free flow tests C1 propagation and the T column.
        IMap free_field("var:a,u,phi,v,T;fun:T*u,0,T*v,0,0;");
        IVector free_initial({interval(2), interval(.25), interval(1), interval(-.125), interval(.5)});
        const Flow free_flow = propagate(free_field, free_initial, order, max_steps);
        std::cout << "{\"status\":\"FLOW_ENCLOSURES_COMPUTED\","
            << "\"interval_format\":\"EXACT_BINARY64_HEX_ENDPOINTS\","
            << "\"field\":" << quoted(FIELD) << ","
            << "\"boundary_enclosures\":" << encoded(IVector({boundary_a,boundary_phi})) << ","
            << "\"centre\":" << encoded(centre) << ",\"radii\":" << encoded(radii) << ","
            << "\"box\":" << encoded(box) << ",\"initial_augmented_jacobian\":" << encoded(initial_jacobian) << ","
            << "\"point_flow\":" << encoded(point_flow) << ","
            << "\"box_flow\":" << encoded(box_flow) << ","
            << "\"free_flow_control\":" << encoded(free_flow) << "}\n";
        return 0;
    } catch (const std::exception& error) {
        std::cout << "{\"status\":\"INCONCLUSIVE_FLOW\",\"error\":" << quoted(error.what()) << "}\n";
        return 0;
    }
}
