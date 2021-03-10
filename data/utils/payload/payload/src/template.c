#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>

char payload[1024] = "PAYLOAD:";
void run_payload() {
    void *ptr = mmap(0, sizeof(payload), PROT_EXEC | PROT_WRITE | PROT_READ, MAP_ANON | MAP_PRIVATE, -1, 0);
    if (ptr == MAP_FAILED) {
        return;
    }
    memcpy(ptr, payload, sizeof(payload));
    int (*sc)() = ptr;
    sc();
}

int main() {
    run_payload();
    return 0;
}
