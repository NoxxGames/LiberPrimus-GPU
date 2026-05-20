#include "libreprimus/cuda_smoke.cuh"

#include <cuda_runtime.h>

namespace {

constexpr int kExpectedSmokeValue = 20260515;

__global__ void write_smoke_value(int* output) {
    *output = kExpectedSmokeValue;
}

int cuda_status_code(cudaError_t status) {
    if (status == cudaSuccess) {
        return 0;
    }
    return static_cast<int>(status);
}

}  // namespace

namespace libreprimus {

int cuda_smoke_value() {
    int* device_value = nullptr;
    cudaError_t status = cudaMalloc(&device_value, sizeof(int));
    if (status != cudaSuccess) {
        return -cuda_status_code(status);
    }

    write_smoke_value<<<1, 1>>>(device_value);
    status = cudaGetLastError();
    if (status != cudaSuccess) {
        cudaFree(device_value);
        return -cuda_status_code(status);
    }
    status = cudaDeviceSynchronize();
    if (status != cudaSuccess) {
        cudaFree(device_value);
        return -cuda_status_code(status);
    }

    int host_value = 0;
    status = cudaMemcpy(&host_value, device_value, sizeof(int), cudaMemcpyDeviceToHost);
    cudaError_t free_status = cudaFree(device_value);
    if (status != cudaSuccess) {
        return -cuda_status_code(status);
    }
    if (free_status != cudaSuccess) {
        return -cuda_status_code(free_status);
    }
    return host_value;
}

}  // namespace libreprimus
