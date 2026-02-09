
#pragma once
#include <Arduino.h>
#include "isa/cpu_middleware.h"

const uint16_t OPCODE = 0x0001;

/**
 ## ADD r16, i16

 @brief Adds a 16-bit immediate value to a 16-bit register.
 @brief
```csharp
add r16, i16
```

 #### Operation:
```csharp
[1] Register dest;
[2] Number src;
[3] 
[4] dest = dest + src;
```

 @class add
 @param api Pointer to the CPU_API safe context instance.
 @param payload The instruction package containing operands.
 @return 
```csharp
void
```

 @note This function handles the addition of a 16-bit immediate value to a specified 16-bit register, updating the register with the result.
 
 @todo Implement flag updates (Zero, Sign, Overflow, Carry, etc.) after the addition operation.
 @todo Add @see references to x86 architecture manuals.

 @date 02/01/2025
 @author Sheñey
 */
void entry(CPU_API *api, InstrPackage payload) noexcept {
    // source : Immediate<arg0>
    uint64_t src = static_cast<uint16_t>(payload.operand.arg0);

    // destination : Register<reg>
    uint64_t dest = api->readRegister(
        payload.modrm.reg,
        CPU_API::RegisterWordLength::WORD,
        CPU_API::getCPURing()
    );

    // Operation : dest + src
    api->writeRegister(
        payload.modrm.reg,
        CPU_API::RegisterWordLength::WORD,
        static_cast<uint16_t>(dest + src),
        CPU_API::getCPURing()
    );
}
