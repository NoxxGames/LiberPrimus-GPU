#include "libreprimus/cuda_smoke.cuh"

#include <cuda_runtime.h>

#include <stdexcept>
#include <string>

namespace {

constexpr int kExpectedSmokeValue = 20260515;

__global__ void write_smoke_value(int* output) {
    *output = kExpectedSmokeValue;
}

void check_cuda(cudaError_t status, const char* operation) {
    if (status != cudaSuccess) {
        throw std::runtime_error(std::string(operation) + " failed: " + cudaGetErrorString(status));
    }
}

}  // namespace

namespace libreprimus {

int cuda_smoke_value() {
    int* device_value = nullptr;
    check_cuda(cudaMalloc(&device_value, sizeof(int)), "cudaMalloc");

    write_smoke_value<<<1, 1>>>(device_value);
    check_cuda(cudaGetLastError(), "write_smoke_value launch");
    check_cuda(cudaDeviceSynchronize(), "cudaDeviceSynchronize");

    int host_value = 0;
    check_cuda(cudaMemcpy(&host_value, device_value, sizeof(int), cudaMemcpyDeviceToHost), "cudaMemcpy");
    check_cuda(cudaFree(device_value), "cudaFree");
    return host_value;
}

}  // namespace libreprimus
