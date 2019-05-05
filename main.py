from enum import Enum, auto
import collections
import io


class AddressMode(Enum):
    Sig8 = auto(),
    Imm8 = auto(),
    Imm16 = auto(),
    ImmX = auto(),
    ImmM = auto(),
    Abs = auto(),
    AbsIdxXInd = auto(),
    AbsIdxX = auto(),
    AbsIdxY = auto(),
    AbsInd = auto(),
    AbsIndLng = auto(),
    AbsLngIdxX = auto(),
    AbsLng = auto(),
    AbsJmp = auto(),
    AbsLngJmp = auto(),
    Acc = auto(),
    BlkMov = auto(),
    DirIdxIndX = auto(),
    DirIdxX = auto(),
    DirIdxY = auto(),
    DirIndIdxY = auto(),
    DirIndLngIdxY = auto(),
    DirIndLng = auto(),
    DirInd = auto(),
    Dir = auto(),
    Imp = auto(),
    RelLng = auto(),
    Rel = auto(),
    Stk = auto(),
    StkRel = auto(),
    StkRelIndIdxY = auto()


class MemoryMode(Enum):
    EIGHT_BIT = auto()
    SIXTEEN_BIT = auto()


ASSEMBLY_OUTPUT_LINE_WIDTH = 60
NUM_BANKS = 8
BANK_SIZE = 0x10000
BANK_START = 0x40

InstructionInfo = collections.namedtuple('InstructionInfo', 'memory_mode index_mode runtime_addr')

hardware_registers = {
    "$2100": "!SCREEN_DISPLAY_REGISTER",
    "$2101": "!OAM_SIZE_AND_DATA_AREA_DESIGNATION",
    "$2102": "!ADDRESS_FOR_ACCESSING_OAM_LOW",
    "$2103": "!ADDRESS_FOR_ACCESSING_OAM_HIGH",
    "$2105": "!BG_MODE_AND_TILE_SIZE_SETTING",
    "$2106": "!MOSAIC_SIZE_AND_BG_ENABLE",
    "$2107": "!BG_1_ADDRESS_AND_SIZE",
    "$2108": "!BG_2_ADDRESS_AND_SIZE",
    "$2109": "!BG_3_ADDRESS_AND_SIZE",
    "$210A": "!BG_4_ADDRESS_AND_SIZE",
    "$210B": "!BG_1_AND_2_TILE_DATA_DESIGNATION",
    "$210C": "!BG_3_AND_4_TILE_DATA_DESIGNATION",
    "$210D": "!BG_1_H_SCROLL_OFFSET",
    "$210E": "!BG_1_V_SCROLL_OFFSET",
    "$210F": "!BG_2_H_SCROLL_OFFSET",
    "$2110": "!BG_2_V_SCROLL_OFFSET",
    "$2111": "!BG_3_H_SCROLL_OFFSET",
    "$2112": "!BG_3_V_SCROLL_OFFSET",
    "$2113": "!BG_4_H_SCROLL_OFFSET",
    "$2114": "!BG_4_V_SCROLL_OFFSET",
    "$2115": "!VRAM_ADDRESS_INCREMENT_VALUE",
    "$2116": "!ADDRESS_FOR_VRAM_READ_WRITE_LOW_BYTE",
    "$2117": "!ADDRESS_FOR_VRAM_READ_WRITE_HIGH_BYTE",
    "$211A": "!INITIAL_SETTING_FOR_MODE_7",
    "$211B": "!MODE_7_MATRIX_PARAMETER_A",
    "$211C": "!MODE_7_MATRIX_PARAMETER_B",
    "$211D": "!MODE_7_MATRIX_PARAMETER_C",
    "$211E": "!MODE_7_MATRIX_PARAMETER_D",
    "$211F": "!MODE_7_CENTER_POSITION_X",
    "$2120": "!MODE_7_CENTER_POSITION_Y",
    "$2121": "!ADDRESS_FOR_CG_RAM_WRITE",
    "$2123": "!BG_1_AND_2_WINDOW_MASK_SETTINGS",
    "$2124": "!BG_3_AND_4_WINDOW_MASK_SETTINGS",
    "$2125": "!OBJ_AND_COLOR_WINDOW_SETTINGS",
    "$2126": "!WINDOW_1_LEFT_POSITION_DESIGNATION",
    "$2127": "!WINDOW_1_RIGHT_POSITION_DESIGNATION",
    "$2128": "!WINDOW_2_LEFT_POSTION_DESIGNATION",
    "$2129": "!WINDOW_2_RIGHT_POSTION_DESIGNATION",
    "$212A": "!BG_1_2_3_4_WINDOW_LOGIC_SETTINGS",
    "$212B": "!COLOR_AND_OBJ_WINDOW_LOGIC_SETTINGS",
    "$212C": "!BG_AND_OBJECT_ENABLE_MAIN_SCREEN",
    "$212D": "!BG_AND_OBJECT_ENABLE_SUB_SCREEN",
    "$212E": "!WINDOW_MASK_DESIGNATION_FOR_MAIN_SCREEN",
    "$212F": "!WINDOW_MASK_DESIGNATION_FOR_SUB_SCREEN",
    "$2130": "!INITIAL_SETTINGS_FOR_COLOR_ADDITION",
    "$2131": "!ADD_SUBTRACT_SELECT_AND_ENABLE",
    "$2132": "!FIXED_COLOR_DATA",
    "$2133": "!SCREEN_INITIAL_SETTINGS",
    "$2140": "!APU_I_O_PORT_0",
    "$2141": "!APU_I_O_PORT_1",
    "$2142": "!APU_I_O_PORT_2",
    "$2143": "!APU_I_O_PORT_3",
    "$4016": "!JOY_A",
    "$4017": "!JOY_B",
    "$4200": "!NMI_V_H_COUNT_AND_JOYPAD_ENABLE",
    "$4201": "!PROGRAMMABLE_I_O_PORT_OUTPUT",
    "$4202": "!MULTIPLICAND_A",
    "$4203": "!MULTIPLIER_B",
    "$4204": "!DIVIDEND_LOW_BYTE",
    "$4205": "!DIVIDEND_HIGH_BYTE",
    "$4206": "!DIVISOR_B",
    "$4207": "!H_COUNT_TIMER",
    "$4208": "!H_COUNT_TIMER_MSB",
    "$4209": "!V_COUNT_TIMER",
    "$420A": "!V_COUNT_TIMER_MSB",
    "$420B": "!REGULAR_DMA_CHANNEL_ENABLE",
    "$420C": "!H_DMA_CHANNEL_ENABLE",
    "$420D": "!CYCLE_SPEED_DESIGNATION",
    "$4210": "!NMI_ENABLE",
    "$4211": "!IRQ_FLAG_BY_H_V_COUNT_TIMER",
    "$4212": "!H_V_BLANK_FLAGS_AND_JOYPAD_STATUS",
    "$4218": "!JOYPAD_1_DATA_LOW_BYTE",
    "$4219": "!JOYPAD_1_DATA_HIGH_BYTE",
    "$421A": "!JOYPAD_2_DATA_LOW_BYTE",
    "$421B": "!JOYPAD_2_DATA_HIGH_BYTE",
    "$421E": "!JOYPAD_4_DATA_LOW_BYTE",
    "$421F": "!JOYPAD_4_DATA_HIGH_BYTE",
    "$4300": "!DMA_0_PARAMS",
    "$4301": "!DMA_0_B_ADDRESS",
    "$4302": "!DMA_0_A_ADDRESS_LOW_BYTE",
    "$4303": "!DMA_0_A_ADDRESS_HIGH_BYTE",
    "$4304": "!DMA_0_A_ADDRESS_BANK",
    "$4305": "!DMA_0_BYTES_COUNT_LOW_BYTE",
    "$4306": "!DMA_0_BYTES_COUNT_HIGH_BYTE",
    "$4310": "!DMA_1_PARAMS",
    "$4311": "!DMA_1_B_ADDRESS",
    "$4312": "!DMA_1_A_ADDRESS_LOW_BYTE",
    "$4313": "!DMA_1_A_ADDRESS_HIGH_BYTE",
    "$4314": "!DMA_1_A_ADDRESS_BANK",
    "$4315": "!DMA_1_BYTES_COUNT_LOW_BYTE",
    "$4316": "!DMA_1_BYTES_COUNT_HIGH_BYTE",
    "$4320": "!DMA_2_PARAMS",
    "$4321": "!DMA_2_B_ADDRESS",
    "$4322": "!DMA_2_A_ADDRESS_LOW_BYTE",
    "$4323": "!DMA_2_A_ADDRESS_HIGH_BYTE",
    "$4324": "!DMA_2_A_ADDRESS_BANK",
    "$4325": "!DMA_2_BYTES_COUNT_LOW_BYTE",
    "$4326": "!DMA_2_BYTES_COUNT_HIGH_BYTE",
    "$4330": "!DMA_3_PARAMS",
    "$4331": "!DMA_3_B_ADDRESS",
    "$4332": "!DMA_3_A_ADDRESS_LOW_BYTE",
    "$4333": "!DMA_3_A_ADDRESS_HIGH_BYTE",
    "$4334": "!DMA_3_A_ADDRESS_BANK",
    "$4335": "!DMA_3_BYTES_COUNT_LOW_BYTE",
    "$4336": "!DMA_3_BYTES_COUNT_HIGH_BYTE",
    "$4340": "!DMA_4_PARAMS",
    "$4341": "!DMA_4_B_ADDRESS",
    "$4342": "!DMA_4_A_ADDRESS_LOW_BYTE",
    "$4343": "!DMA_4_A_ADDRESS_HIGH_BYTE",
    "$4344": "!DMA_4_A_ADDRESS_BANK",
    "$4345": "!DMA_4_BYTES_COUNT_LOW_BYTE",
    "$4346": "!DMA_4_BYTES_COUNT_HIGH_BYTE",
    "$4350": "!DMA_5_PARAMS",
    "$4351": "!DMA_5_B_ADDRESS",
    "$4352": "!DMA_5_A_ADDRESS_LOW_BYTE ",
    "$4353": "!DMA_5_A_ADDRESS_HIGH_BYTE",
    "$4354": "!DMA_5_A_ADDRESS_BANK",
    "$4355": "!DMA_5_BYTES_COUNT_LOW_BYTE",
    "$4356": "!DMA_5_BYTES_COUNT_HIGH_BYTE",
    "$4360": "!DMA_6_PARAMS",
    "$4361": "!DMA_6_B_ADDRESS",
    "$4362": "!DMA_6_A_ADDRESS_LOW_BYTE",
    "$4363": "!DMA_6_A_ADDRESS_HIGH_BYTE",
    "$4364": "!DMA_6_A_ADDRESS_BANK",
    "$4365": "!DMA_6_BYTES_COUNT_LOW_BYTE",
    "$4366": "!DMA_6_BYTES_COUNT_HIGH_BYTE",
    "$4370": "!DMA_7_PARAMS",
    "$4371": "!DMA_7_B_ADDRESS",
    "$4372": "!DMA_7_A_ADDRESS_LOW_BYTE",
    "$4373": "!DMA_7_A_ADDRESS_HIGH_BYTE",
    "$4374": "!DMA_7_A_ADDRESS_BANK",
    "$4375": "!DMA_7_BYTES_COUNT_LOW_BYTE",
    "$4376": "!DMA_7_BYTES_COUNT_HIGH_BYTE",
    "$4216": "!PRODUCT_REMAINDER_RESULT_LOW_BYTE",
    "$2118": "!DATA_FOR_VRAM_WRITE_LOW_BYTE",
    "$4214": "!QUOTIENT_OF_DIVIDE_RESULT_LOW_BYTE",
    "$006000": "!DSP1_DATA_REGISTER",
    "$007000": "!DSP1_STATUS_REGISTER"
}


def get_operand_size(addr_mode, current_memory_mode, current_index_mode):
    if addr_mode in [AddressMode.Acc, AddressMode.Imp, AddressMode.Stk]:
        return 1
    elif addr_mode in [AddressMode.DirIdxIndX, AddressMode.DirIdxX, AddressMode.DirIdxY, AddressMode.DirIndIdxY,
                       AddressMode.DirIndLngIdxY, AddressMode.DirIndLng, AddressMode.DirInd, AddressMode.Dir,
                       AddressMode.Sig8, AddressMode.Imm8, AddressMode.Rel, AddressMode.StkRel,
                       AddressMode.StkRelIndIdxY]:
        return 2
    elif addr_mode in [AddressMode.Abs, AddressMode.AbsIdxXInd, AddressMode.AbsIdxX, AddressMode.AbsIdxY,
                       AddressMode.AbsInd,
                       AddressMode.AbsIndLng, AddressMode.AbsJmp, AddressMode.BlkMov, AddressMode.Imm16,
                       AddressMode.RelLng]:
        return 3
    elif addr_mode in [AddressMode.AbsLngJmp, AddressMode.AbsLngIdxX, AddressMode.AbsLng]:
        return 4

    if addr_mode is AddressMode.ImmX:
        return 2 if current_index_mode is MemoryMode.EIGHT_BIT else 3
    elif addr_mode is AddressMode.ImmM:
        return 2 if current_memory_mode is MemoryMode.EIGHT_BIT else 3


def open_rom(file):
    with open(file, 'rb') as f:
        data = f.read()
        return data


def open_executed_instruction_addresses(file):
    with open(file, 'r') as f:
        data = []
        for line in f:
            memory_mode_and_addr = line.split(" ")
            assert len(memory_mode_and_addr) == 3
            memory_mode = int(memory_mode_and_addr[0])
            index_mode = int(memory_mode_and_addr[1])
            runtime_addr = int(memory_mode_and_addr[2])

            data.append(InstructionInfo(memory_mode=memory_mode, index_mode=index_mode, runtime_addr=runtime_addr))
        return data


def get_bank_and_offset(addr):
    bank = (addr & 0xFF0000) >> 16
    bank_offset = (addr & 0x00FFFF)
    return bank, bank_offset


def convert_runtime_address_to_rom(addr):
    bank, bank_offset = get_bank_and_offset(addr)

    if addr < 0x400000:
        return addr, bank, bank_offset

    if 0x40 <= bank <= 0x7d:
        adjusted_address = addr - 0x400000
        bank, bank_offset = get_bank_and_offset(adjusted_address)
    elif 0x80 <= bank <= 0x9f:
        adjusted_address = addr - 0x800000
        bank, bank_offset = get_bank_and_offset(adjusted_address)
    elif 0xa0 <= bank <= 0xbf:
        adjusted_address = addr - 0xa00000 + 0x200000
        bank, bank_offset = get_bank_and_offset(adjusted_address)
    elif 0xc0 <= bank <= 0xfd:
        adjusted_address = addr - 0xc00000
        bank, bank_offset = get_bank_and_offset(adjusted_address)
    elif 0xfe <= bank <= 0xff:
        adjusted_address = addr - 0xc00000
        bank, bank_offset = get_bank_and_offset(adjusted_address)
    else:
        assert False

    return adjusted_address, bank, bank_offset


def get_operand(addr_mode, rom_data, operand_size):
    if operand_size == 2:
        return rom_data[1]
    elif operand_size == 3:
        return rom_data[2] << 8 | rom_data[1]
    elif operand_size == 4:
        return rom_data[3] << 16 | rom_data[2] << 8 | rom_data[1]

    return None


def handle_Sig8(v, size=0):
    return f"#${v:0{2}X}"


def handle_Imm8(v, size=0):
    return f"#${v:0{2}X}"


def handle_Imm16(v, size=0):
    return f"${v:0{4}X}"


def handle_ImmX(v, size):
    if size == 2:
        return (f"#${v:0{2}X}")
    else:
        return f"#${v:0{4}X}"


def handle_ImmM(v, size):
    if size == 2:
        return (f"#${v:0{2}X}")
    else:
        return f"#${v:0{4}X}"


def handle_Abs(v, size=0):
    return f"${v:0{4}X}"


def handle_AbsIdxXInd(v, size=0):
    return f"(${v:0{4}X},x)"


def handle_AbsIdxX(v, size=0):
    return f"${v:0{4}X},x"


def handle_AbsIdxY(v, size=0):
    return f"${v:0{4}X},y"


def handle_AbsInd(v, size=0):
    return f"(${v:0{4}X})"


def handle_AbsIndLng(v, size=0):
    return f"[${v:0{4}X}]"


def handle_AbsLngIdxX(v, size=0):
    return f"${v:0{6}X},x"


def handle_AbsLng(v, size=0):
    return f"${v:0{6}X}"


def handle_AbsJmp(v, size=0):
    return f"(${v:0{4}X})"


def handle_AbsLngJmp(v, size=0):
    return f"${v:0{6}X}"


def handle_Acc(v, size=0):
    pass


def handle_BlkMov(v, size=0):
    p1 = v & 0x00FF
    p2 = (v & 0xFF00) >> 8

    return f"${p1:0{2}X},${p2:0{2}X}"


def handle_DirIdxIndX(v, size=0):
    return f"(${v:0{2}X},x)"


def handle_DirIdxX(v, size=0):
    return f"${v:0{2}X},x"


def handle_DirIdxY(v, size=0):
    return f"${v:0{2}X},y"


def handle_DirIndIdxY(v, size=0):
    return f"(${v:0{2}X}),y"


def handle_DirIndLngIdxY(v, size=0):
    return f"[${v:0{2}X}],y"


def handle_DirIndLng(v, size=0):
    return f"[${v:0{2}X}]"


def handle_DirInd(v, size=0):
    return f"(${v:0{2}X})"


def handle_Dir(v, size=0):
    return f"${v:0{2}X}"


def handle_Imp(v):
    pass


def handle_RelLng(v, size=0):
    return f"${v:0{4}X}"


def handle_Rel(v, size=0):
    return f"${v:0{2}X}"


def handle_Stk(v, size=0):
    pass


def handle_StkRel(v, size=0):
    return f"${v:0{2}X},s"


def handle_StkRelIndIdxY(v, size=0):
    return f"(${v:0{2}X},s),y"


address_mode_dispatch = {AddressMode.Sig8: handle_Sig8,
                         AddressMode.Imm8: handle_Imm8,
                         AddressMode.Imm16: handle_Imm16,
                         AddressMode.ImmX: handle_ImmX,
                         AddressMode.ImmM: handle_ImmM,
                         AddressMode.Abs: handle_Abs,
                         AddressMode.AbsIdxXInd: handle_AbsIdxXInd,
                         AddressMode.AbsIdxX: handle_AbsIdxX,
                         AddressMode.AbsIdxY: handle_AbsIdxY,
                         AddressMode.AbsInd: handle_AbsInd,
                         AddressMode.AbsIndLng: handle_AbsIndLng,
                         AddressMode.AbsLngIdxX: handle_AbsLngIdxX,
                         AddressMode.AbsLng: handle_AbsLng,
                         AddressMode.AbsJmp: handle_AbsJmp,
                         AddressMode.AbsLngJmp: handle_AbsLngJmp,
                         AddressMode.Acc: handle_Acc,
                         AddressMode.BlkMov: handle_BlkMov,
                         AddressMode.DirIdxIndX: handle_DirIdxIndX,
                         AddressMode.DirIdxX: handle_DirIdxX,
                         AddressMode.DirIdxY: handle_DirIdxY,
                         AddressMode.DirIndIdxY: handle_DirIndIdxY,
                         AddressMode.DirIndLngIdxY: handle_DirIndLngIdxY,
                         AddressMode.DirIndLng: handle_DirIndLng,
                         AddressMode.DirInd: handle_DirInd,
                         AddressMode.Dir: handle_Dir,
                         AddressMode.Imp: handle_Imp,
                         AddressMode.RelLng: handle_RelLng,
                         AddressMode.Rel: handle_Rel,
                         AddressMode.Stk: handle_Stk,
                         AddressMode.StkRel: handle_StkRel,
                         AddressMode.StkRelIndIdxY: handle_StkRelIndIdxY}

opcode_address_modes = [AddressMode.Sig8, AddressMode.DirIdxIndX, AddressMode.Sig8, AddressMode.StkRel, AddressMode.Dir,
                        AddressMode.Dir, AddressMode.Dir, AddressMode.DirIndLng, AddressMode.Stk, AddressMode.ImmM,
                        AddressMode.Acc,
                        AddressMode.Stk, AddressMode.Abs, AddressMode.Abs, AddressMode.Abs, AddressMode.AbsLng,
                        AddressMode.Rel, AddressMode.DirIndIdxY, AddressMode.DirInd, AddressMode.StkRelIndIdxY,
                        AddressMode.Dir, AddressMode.DirIdxX, AddressMode.DirIdxX, AddressMode.DirIndLngIdxY,
                        AddressMode.Imp, AddressMode.AbsIdxY, AddressMode.Acc, AddressMode.Imp, AddressMode.Abs,
                        AddressMode.AbsIdxX, AddressMode.AbsIdxX, AddressMode.AbsLngIdxX,
                        AddressMode.Abs, AddressMode.DirIdxIndX, AddressMode.AbsLng, AddressMode.StkRel,
                        AddressMode.Dir, AddressMode.Dir, AddressMode.Dir, AddressMode.DirIndLng, AddressMode.Stk,
                        AddressMode.ImmM, AddressMode.Acc,
                        AddressMode.Stk, AddressMode.Abs, AddressMode.Abs, AddressMode.Abs, AddressMode.AbsLng,
                        AddressMode.Rel, AddressMode.DirIndIdxY, AddressMode.DirInd, AddressMode.StkRelIndIdxY,
                        AddressMode.DirIdxX, AddressMode.DirIdxX, AddressMode.DirIdxX,
                        AddressMode.DirIndLngIdxY, AddressMode.Imp, AddressMode.AbsIdxY, AddressMode.Acc,
                        AddressMode.Imp, AddressMode.AbsIdxX, AddressMode.AbsIdxX, AddressMode.AbsIdxX,
                        AddressMode.AbsLngIdxX,
                        AddressMode.Stk, AddressMode.DirIdxIndX, AddressMode.Imm8, AddressMode.StkRel,
                        AddressMode.BlkMov, AddressMode.Dir, AddressMode.Dir, AddressMode.DirIndLng, AddressMode.Stk,
                        AddressMode.ImmM,
                        AddressMode.Acc, AddressMode.Stk, AddressMode.Abs, AddressMode.Abs, AddressMode.Abs,
                        AddressMode.AbsLng,
                        AddressMode.Rel, AddressMode.DirIndIdxY, AddressMode.DirInd, AddressMode.StkRelIndIdxY,
                        AddressMode.BlkMov, AddressMode.DirIdxX, AddressMode.DirIdxX, AddressMode.DirIndLngIdxY,
                        AddressMode.Imp, AddressMode.AbsIdxY, AddressMode.Stk, AddressMode.Imp, AddressMode.AbsLng,
                        AddressMode.AbsIdxX, AddressMode.AbsIdxX, AddressMode.AbsLngIdxX,
                        AddressMode.Stk, AddressMode.DirIdxIndX, AddressMode.RelLng, AddressMode.StkRel,
                        AddressMode.Dir, AddressMode.Dir, AddressMode.Dir, AddressMode.DirIndLng, AddressMode.Stk,
                        AddressMode.ImmM, AddressMode.Acc,
                        AddressMode.Stk, AddressMode.AbsInd, AddressMode.Abs, AddressMode.Abs, AddressMode.AbsLng,
                        AddressMode.Rel, AddressMode.DirIndIdxY, AddressMode.DirInd, AddressMode.StkRelIndIdxY,
                        AddressMode.DirIdxX, AddressMode.DirIdxX, AddressMode.DirIdxX,
                        AddressMode.DirIndLngIdxY, AddressMode.Imp, AddressMode.AbsIdxY, AddressMode.Stk,
                        AddressMode.Imp, AddressMode.AbsIdxXInd, AddressMode.AbsIdxX, AddressMode.AbsIdxX,
                        AddressMode.AbsLngIdxX,
                        AddressMode.Rel, AddressMode.DirIdxIndX, AddressMode.RelLng, AddressMode.StkRel,
                        AddressMode.Dir, AddressMode.Dir, AddressMode.Dir, AddressMode.DirIndLng, AddressMode.Imp,
                        AddressMode.ImmM, AddressMode.Imp,
                        AddressMode.Stk, AddressMode.Abs, AddressMode.Abs, AddressMode.Abs, AddressMode.AbsLng,
                        AddressMode.Rel, AddressMode.DirIndIdxY, AddressMode.DirInd, AddressMode.StkRelIndIdxY,
                        AddressMode.DirIdxX, AddressMode.DirIdxX, AddressMode.DirIdxY,
                        AddressMode.DirIndLngIdxY, AddressMode.Imp, AddressMode.AbsIdxY, AddressMode.Imp,
                        AddressMode.Imp, AddressMode.Abs, AddressMode.AbsIdxX, AddressMode.AbsIdxX,
                        AddressMode.AbsLngIdxX,
                        AddressMode.ImmX, AddressMode.DirIdxIndX, AddressMode.ImmX, AddressMode.StkRel, AddressMode.Dir,
                        AddressMode.Dir, AddressMode.Dir, AddressMode.DirIndLng, AddressMode.Imp, AddressMode.ImmM,
                        AddressMode.Imp,
                        AddressMode.Stk, AddressMode.Abs, AddressMode.Abs, AddressMode.Abs, AddressMode.AbsLng,
                        AddressMode.Rel, AddressMode.DirIndIdxY, AddressMode.DirInd, AddressMode.StkRelIndIdxY,
                        AddressMode.DirIdxX, AddressMode.DirIdxX, AddressMode.DirIdxY,
                        AddressMode.DirIndLngIdxY, AddressMode.Imp, AddressMode.AbsIdxY, AddressMode.Imp,
                        AddressMode.Imp, AddressMode.AbsIdxX, AddressMode.AbsIdxX, AddressMode.AbsIdxY,
                        AddressMode.AbsLngIdxX,
                        AddressMode.ImmX, AddressMode.DirIdxIndX, AddressMode.Imm8, AddressMode.StkRel, AddressMode.Dir,
                        AddressMode.Dir, AddressMode.Dir, AddressMode.DirIndLng, AddressMode.Imp, AddressMode.ImmM,
                        AddressMode.Imp,
                        AddressMode.Imp, AddressMode.Abs, AddressMode.Abs, AddressMode.Abs, AddressMode.AbsLng,
                        AddressMode.Rel, AddressMode.DirIndIdxY, AddressMode.DirInd, AddressMode.StkRelIndIdxY,
                        AddressMode.Dir, AddressMode.DirIdxX, AddressMode.DirIdxX, AddressMode.DirIndLngIdxY,
                        AddressMode.Imp, AddressMode.AbsIdxY, AddressMode.Stk, AddressMode.Imp, AddressMode.AbsIndLng,
                        AddressMode.AbsIdxX, AddressMode.AbsIdxX, AddressMode.AbsLngIdxX,
                        AddressMode.ImmX, AddressMode.DirIdxIndX, AddressMode.Imm8, AddressMode.StkRel, AddressMode.Dir,
                        AddressMode.Dir, AddressMode.Dir, AddressMode.DirIndLng, AddressMode.Imp, AddressMode.ImmM,
                        AddressMode.Imp,
                        AddressMode.Imp, AddressMode.Abs, AddressMode.Abs, AddressMode.Abs, AddressMode.AbsLng,
                        AddressMode.Rel, AddressMode.DirIndIdxY, AddressMode.DirInd, AddressMode.StkRelIndIdxY,
                        AddressMode.Imm16, AddressMode.DirIdxX, AddressMode.DirIdxX, AddressMode.DirIndLngIdxY,
                        AddressMode.Imp, AddressMode.AbsIdxY, AddressMode.Stk, AddressMode.Imp, AddressMode.AbsIdxXInd,
                        AddressMode.AbsIdxX, AddressMode.AbsIdxX, AddressMode.AbsLngIdxX]

opcodes = ["BRK", "ORA", "COP", "ORA", "TSB", "ORA", "ASL", "ORA", "PHP", "ORA", "ASL", "PHD", "TSB", "ORA", "ASL",
           "ORA",
           "BPL", "ORA", "ORA", "ORA", "TRB", "ORA", "ASL", "ORA", "CLC", "ORA", "INC", "TCS", "TRB", "ORA", "ASL",
           "ORA",
           "JSR", "AND", "JSL", "AND", "BIT", "AND", "ROL", "AND", "PLP", "AND", "ROL", "PLD", "BIT", "AND", "ROL",
           "AND",
           "BMI", "AND", "AND", "AND", "BIT", "AND", "ROL", "AND", "SEC", "AND", "DEC", "TSC", "BIT", "AND", "ROL",
           "AND",
           "RTI", "EOR", "WDM", "EOR", "MVP", "EOR", "LSR", "EOR", "PHA", "EOR", "LSR", "PHK", "JMP", "EOR", "LSR",
           "EOR",
           "BVC", "EOR", "EOR", "EOR", "MVN", "EOR", "LSR", "EOR", "CLI", "EOR", "PHY", "TCD", "JMP", "EOR", "LSR",
           "EOR",
           "RTS", "ADC", "PER", "ADC", "STZ", "ADC", "ROR", "ADC", "PLA", "ADC", "ROR", "RTL", "JMP", "ADC", "ROR",
           "ADC",
           "BVS", "ADC", "ADC", "ADC", "STZ", "ADC", "ROR", "ADC", "SEI", "ADC", "PLY", "TDC", "JMP", "ADC", "ROR",
           "ADC",
           "BRA", "STA", "BRL", "STA", "STY", "STA", "STX", "STA", "DEY", "BIT", "TXA", "PHB", "STY", "STA", "STX",
           "STA",
           "BCC", "STA", "STA", "STA", "STY", "STA", "STX", "STA", "TYA", "STA", "TXS", "TXY", "STZ", "STA", "STZ",
           "STA",
           "LDY", "LDA", "LDX", "LDA", "LDY", "LDA", "LDX", "LDA", "TAY", "LDA", "TAX", "PLB", "LDY", "LDA", "LDX",
           "LDA",
           "BCS", "LDA", "LDA", "LDA", "LDY", "LDA", "LDX", "LDA", "CLV", "LDA", "TSX", "TYX", "LDY", "LDA", "LDX",
           "LDA",
           "CPY", "CMP", "REP", "CMP", "CPY", "CMP", "DEC", "CMP", "INY", "CMP", "DEX", "WAI", "CPY", "CMP", "DEC",
           "CMP",
           "BNE", "CMP", "CMP", "CMP", "PEI", "CMP", "DEC", "CMP", "CLD", "CMP", "PHX", "STP", "JML", "CMP", "DEC",
           "CMP",
           "CPX", "SBC", "SEP", "SBC", "CPX", "SBC", "INC", "SBC", "INX", "SBC", "NOP", "XBA", "CPX", "SBC", "INC",
           "SBC",
           "BEQ", "SBC", "SBC", "SBC", "PEA", "SBC", "INC", "SBC", "SED", "SBC", "PLX", "XCE", "JSR", "SBC", "INC",
           "SBC"]


def get_addr_mode_from_opcode_value(opcode_value):
    return opcode_address_modes[opcode_value]


class Data:
    def __init__(self, value=0xff):
        self.value = value

    def render(self, output, bank_num, bank_offset):
        comment_addr = bank_num | bank_offset
        comment_string = f"; ${comment_addr:0{6}X}\n"
        assembly_string = f"\tdb ${self.value:0{2}X}"
        width = ASSEMBLY_OUTPUT_LINE_WIDTH - len(assembly_string)
        output.write(f"{assembly_string}{comment_string:>{width}}")


class Instruction:
    def __init__(self, opcode, current_memory_mode, current_index_mode, rom_data_from_opcode_addr):
        addr_mode = get_addr_mode_from_opcode_value(opcode)
        self.opcode = opcode
        self.operand_size = get_operand_size(addr_mode, current_memory_mode, current_index_mode)
        self.addr_mode = addr_mode
        self.operand = get_operand(addr_mode, rom_data_from_opcode_addr, self.operand_size)
        self.memory_mode = current_memory_mode
        self.index_mode = current_index_mode

    def render(self, output, bank_num, bank_offset):
        comment_addr = bank_num | bank_offset
        comment_string = f"; ${comment_addr:0{6}X}\n"
        opcode_string = f"\t{opcodes[self.opcode]}"
        if self.operand is None:
            width = ASSEMBLY_OUTPUT_LINE_WIDTH - len(opcode_string)
            output.write(f"{opcode_string}{comment_string:>{width}}")
        else:
            operand_string = address_mode_dispatch[self.addr_mode](self.operand, self.operand_size)
            if operand_string in hardware_registers:
                operand_string = hardware_registers[operand_string]
            width = ASSEMBLY_OUTPUT_LINE_WIDTH - (len(opcode_string) + len(operand_string) + 1)
            output.write(f"{opcode_string} {operand_string}{comment_string:>{width}}")


class InstructionOperand:
    def __init__(self, value):
        self.value = value

    def render(self, output, bank_num, bank_offset):
        pass


class Bank:
    def __init__(self, bank_index):
        self.payload = [None for _ in range(BANK_SIZE)]
        self.bank_num = (BANK_START + bank_index) << 16

    def render(self, output):
        for (bank_offset, payload) in enumerate(self.payload):
            if payload is not None:
                payload.render(output, self.bank_num, bank_offset)


class Disassembly:
    def __init__(self):
        self.banks = [Bank(i) for i in range(NUM_BANKS)]

    def mark_as_data(self, bank, bank_offset, data):
        self.banks[bank].payload[bank_offset] = Data(data)

    def mark_as_instruction(self, bank, bank_offset, opcode, current_memory_mode, current_index_mode,
                            rom_data_from_opcode_addr):
        # detect the case where the original assembly employed space saving technique utilising part of the previous
        # instruction operand as the opcode.
        # if the address we were going to write the instruction to is part of a previous InstructionOperand
        # then we bail out as we want to leave this bit as data to be able to reassemble
        if isinstance(self.banks[bank].payload[bank_offset], InstructionOperand):
            return False

        addr_mode = get_addr_mode_from_opcode_value(opcode)
        operand_size = get_operand_size(addr_mode, current_memory_mode, current_index_mode)
        for i in range(operand_size):
            if isinstance(self.banks[bank].payload[bank_offset + i], Instruction):
                return False

        self.banks[bank].payload[bank_offset] = Instruction(opcode=opcode,
                                                            current_memory_mode=current_memory_mode,
                                                            current_index_mode=current_index_mode,
                                                            rom_data_from_opcode_addr=rom_data_from_opcode_addr)
        for i in range(1, operand_size):
            self.banks[bank].payload[bank_offset + i] = InstructionOperand(rom_data_from_opcode_addr[i])

        return True

    def disassemble_branches_not_taken(self, rom):
        for index in range(len(self.banks)):
            for offset in range(len(self.banks[index].payload)):
                if isinstance(self.banks[index].payload[offset], Instruction):
                    instruction = self.banks[index].payload[offset]
                    current_memory_mode = instruction.memory_mode
                    current_index_mode = instruction.index_mode
                    if opcodes[instruction.opcode] in ["BNE", "BPL", "BMI", "BVC", "BCS", "BEQ","BCC", "BVS"]:
                        size = instruction.operand_size
                        next_instruction_offset = offset + size
                        while isinstance(self.banks[index].payload[next_instruction_offset], Data):
                            rom_addr = (index * BANK_SIZE) + next_instruction_offset
                            disassembled_instruction = self.mark_as_instruction(bank=index,
                                                                                bank_offset=next_instruction_offset,
                                                                                opcode=rom[rom_addr],
                                                                                current_memory_mode=current_memory_mode,
                                                                                current_index_mode=current_index_mode,
                                                                                rom_data_from_opcode_addr=rom[
                                                                                                          rom_addr:])

                            if disassembled_instruction:
                                # check to see if we did a REP or SEP which could have changed the memory or index mode.
                                instruction = self.banks[index].payload[next_instruction_offset]
                                mnemonic = opcodes[instruction.opcode]
                                if mnemonic is "REP":
                                    instruction_operand = self.banks[index].payload[next_instruction_offset + 1]
                                    assert isinstance(instruction_operand, InstructionOperand)
                                    current_memory_mode = MemoryMode.SIXTEEN_BIT if (instruction_operand.value & 0b00100000) else current_memory_mode
                                    current_index_mode = MemoryMode.SIXTEEN_BIT if (instruction_operand.value & 0b00010000) else current_index_mode
                                    instruction.memory_mode = current_memory_mode
                                    instruction.index_mode = current_index_mode
                                elif mnemonic is "SEP":
                                    instruction_operand = self.banks[index].payload[next_instruction_offset + 1]
                                    assert isinstance(instruction_operand, InstructionOperand)
                                    current_memory_mode = MemoryMode.EIGHT_BIT if (instruction_operand.value & 0b00100000) else current_memory_mode
                                    current_index_mode = MemoryMode.EIGHT_BIT if (instruction_operand.value & 0b00010000) else current_index_mode
                                    instruction.memory_mode = current_memory_mode
                                    instruction.index_mode = current_index_mode

                                assert isinstance(self.banks[index].payload[next_instruction_offset], Instruction)
                                assert opcodes[self.banks[index].payload[next_instruction_offset].opcode] is not "XCE"
                                next_instruction_offset += self.banks[index].payload[next_instruction_offset].operand_size
                            else:
                                break

    def render(self):
        for (bank_index, bank) in enumerate(self.banks):
            bank_output = io.StringIO()
            code_addr = (BANK_START + bank_index) << 16
            if bank_index == 0:
                bank_output.write(f"hirom\n\norg ${code_addr:0{6}X}\n\narch 65816\n\n")
            else:
                bank_output.write(f"org ${code_addr:0{6}X}\n\n")
            bank.render(bank_output)
            with open(f"bank{bank_index:0{2}d}.asm", 'w') as f:
                f.write(bank_output.getvalue())


if __name__ == "__main__":
    rom = open_rom("Super Mario Kart (USA).sfc")
    disassembly = Disassembly()
    for (addr, d) in enumerate(rom):
        bank, bank_offset = get_bank_and_offset(addr)
        disassembly.mark_as_data(bank=bank, bank_offset=bank_offset, data=d)

    current_memory_mode = MemoryMode.EIGHT_BIT
    current_index_mode = MemoryMode.EIGHT_BIT
    executed_instruction_info = open_executed_instruction_addresses("instruction_trace.txt")
    for instruction_info in executed_instruction_info:
        current_memory_mode = MemoryMode.EIGHT_BIT if instruction_info.memory_mode is 1 else MemoryMode.SIXTEEN_BIT
        current_index_mode = MemoryMode.SIXTEEN_BIT if instruction_info.index_mode is 1 else MemoryMode.SIXTEEN_BIT
        rom_addr, bank, bank_offset = convert_runtime_address_to_rom(instruction_info.runtime_addr)

        opcode_value = rom[rom_addr]
        disassembly.mark_as_instruction(bank=bank, bank_offset=bank_offset, opcode=opcode_value,
                                        current_memory_mode=current_memory_mode, current_index_mode=current_index_mode,
                                        rom_data_from_opcode_addr=rom[rom_addr:])

    disassembly.disassemble_branches_not_taken(rom)
    disassembly.render()
