
#pragma once
#include <Arduino.h>
#include "isa/cpu_middleware.h"

/**
 ## MOV r16, r16
 @brief Moves the value from one 16-bit register to another 16-bit register.
 @brief
```csharp
mov r16, r16
```
 
 @class mov
 @param api Pointer to the CPU_API safe context instance.
 @param payload The instruction package containing operands.
 @return
```csharp
[1] Register dest;
[2] Register src;
[3] 
[4] dest = src;
```

 @note This function handles the transfer of data between two 16-bit registers.

 @todo Add @see references to x86 architecture manuals.

 @date 02/01/2025
 @author Sheñey
 */
inline void reg16_reg16(CPU_API *api, InstrPackage payload) noexcept {
    // source : Register<rm>
    uint64_t src = api->readRegister(
        payload.modrm.rm,
        CPU_API::RegisterWordLength::WORD,
        CPU_API::getCPURing()
    );

    // destination : Register<reg>
    api->writeRegister(
        payload.modrm.reg,
        CPU_API::RegisterWordLength::WORD,
        static_cast<uint16_t>(src),
        CPU_API::getCPURing()
    );
}
