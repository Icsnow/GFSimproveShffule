\ Model DS-MITM
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  TypeZ[0,0] + TypeZ[0,1] + TypeZ[0,2] + TypeZ[1,0] + TypeZ[1,1]
   + TypeZ[1,2] + TypeZ[2,0] + TypeZ[2,1] + TypeZ[2,2] + TypeZ[3,0]
   + TypeZ[3,1] + TypeZ[3,2] + TypeZ[4,0] + TypeZ[4,1] + TypeZ[4,2]
   + TypeZ[5,0] + TypeZ[5,1] + TypeZ[5,2] + TypeZ[6,0] + TypeZ[6,1]
   + TypeZ[6,2] + TypeZ[7,0] + TypeZ[7,1] + TypeZ[7,2]
Subject To
 R0: TypeX[0,0] + TypeX[0,1] - TypeX[1,4] >= 0
 R1: - TypeX[0,0] - TypeX[0,1] + 2 TypeX[1,4] >= 0
 R2: TypeX[0,2] + TypeX[0,3] - TypeX[1,0] >= 0
 R3: - TypeX[0,2] - TypeX[0,3] + 2 TypeX[1,0] >= 0
 R4: TypeX[0,4] + TypeX[0,5] - TypeX[1,2] >= 0
 R5: - TypeX[0,4] - TypeX[0,5] + 2 TypeX[1,2] >= 0
 R6: TypeX[0,0] - TypeX[1,1] = 0
 R7: TypeX[0,2] - TypeX[1,3] = 0
 R8: TypeX[0,4] - TypeX[1,5] = 0
 R9: TypeX[1,0] + TypeX[1,1] - TypeX[2,4] >= 0
 R10: - TypeX[1,0] - TypeX[1,1] + 2 TypeX[2,4] >= 0
 R11: TypeX[1,2] + TypeX[1,3] - TypeX[2,0] >= 0
 R12: - TypeX[1,2] - TypeX[1,3] + 2 TypeX[2,0] >= 0
 R13: TypeX[1,4] + TypeX[1,5] - TypeX[2,2] >= 0
 R14: - TypeX[1,4] - TypeX[1,5] + 2 TypeX[2,2] >= 0
 R15: TypeX[1,0] - TypeX[2,1] = 0
 R16: TypeX[1,2] - TypeX[2,3] = 0
 R17: TypeX[1,4] - TypeX[2,5] = 0
 R18: TypeX[2,0] + TypeX[2,1] - TypeX[3,4] >= 0
 R19: - TypeX[2,0] - TypeX[2,1] + 2 TypeX[3,4] >= 0
 R20: TypeX[2,2] + TypeX[2,3] - TypeX[3,0] >= 0
 R21: - TypeX[2,2] - TypeX[2,3] + 2 TypeX[3,0] >= 0
 R22: TypeX[2,4] + TypeX[2,5] - TypeX[3,2] >= 0
 R23: - TypeX[2,4] - TypeX[2,5] + 2 TypeX[3,2] >= 0
 R24: TypeX[2,0] - TypeX[3,1] = 0
 R25: TypeX[2,2] - TypeX[3,3] = 0
 R26: TypeX[2,4] - TypeX[3,5] = 0
 R27: TypeX[3,0] + TypeX[3,1] - TypeX[4,4] >= 0
 R28: - TypeX[3,0] - TypeX[3,1] + 2 TypeX[4,4] >= 0
 R29: TypeX[3,2] + TypeX[3,3] - TypeX[4,0] >= 0
 R30: - TypeX[3,2] - TypeX[3,3] + 2 TypeX[4,0] >= 0
 R31: TypeX[3,4] + TypeX[3,5] - TypeX[4,2] >= 0
 R32: - TypeX[3,4] - TypeX[3,5] + 2 TypeX[4,2] >= 0
 R33: TypeX[3,0] - TypeX[4,1] = 0
 R34: TypeX[3,2] - TypeX[4,3] = 0
 R35: TypeX[3,4] - TypeX[4,5] = 0
 R36: TypeX[4,0] + TypeX[4,1] - TypeX[5,4] >= 0
 R37: - TypeX[4,0] - TypeX[4,1] + 2 TypeX[5,4] >= 0
 R38: TypeX[4,2] + TypeX[4,3] - TypeX[5,0] >= 0
 R39: - TypeX[4,2] - TypeX[4,3] + 2 TypeX[5,0] >= 0
 R40: TypeX[4,4] + TypeX[4,5] - TypeX[5,2] >= 0
 R41: - TypeX[4,4] - TypeX[4,5] + 2 TypeX[5,2] >= 0
 R42: TypeX[4,0] - TypeX[5,1] = 0
 R43: TypeX[4,2] - TypeX[5,3] = 0
 R44: TypeX[4,4] - TypeX[5,5] = 0
 R45: TypeX[5,0] + TypeX[5,1] - TypeX[6,4] >= 0
 R46: - TypeX[5,0] - TypeX[5,1] + 2 TypeX[6,4] >= 0
 R47: TypeX[5,2] + TypeX[5,3] - TypeX[6,0] >= 0
 R48: - TypeX[5,2] - TypeX[5,3] + 2 TypeX[6,0] >= 0
 R49: TypeX[5,4] + TypeX[5,5] - TypeX[6,2] >= 0
 R50: - TypeX[5,4] - TypeX[5,5] + 2 TypeX[6,2] >= 0
 R51: TypeX[5,0] - TypeX[6,1] = 0
 R52: TypeX[5,2] - TypeX[6,3] = 0
 R53: TypeX[5,4] - TypeX[6,5] = 0
 R54: TypeX[6,0] + TypeX[6,1] - TypeX[7,4] >= 0
 R55: - TypeX[6,0] - TypeX[6,1] + 2 TypeX[7,4] >= 0
 R56: TypeX[6,2] + TypeX[6,3] - TypeX[7,0] >= 0
 R57: - TypeX[6,2] - TypeX[6,3] + 2 TypeX[7,0] >= 0
 R58: TypeX[6,4] + TypeX[6,5] - TypeX[7,2] >= 0
 R59: - TypeX[6,4] - TypeX[6,5] + 2 TypeX[7,2] >= 0
 R60: TypeX[6,0] - TypeX[7,1] = 0
 R61: TypeX[6,2] - TypeX[7,3] = 0
 R62: TypeX[6,4] - TypeX[7,5] = 0
 R63: TypeX[7,0] + TypeX[7,1] - TypeX[8,4] >= 0
 R64: - TypeX[7,0] - TypeX[7,1] + 2 TypeX[8,4] >= 0
 R65: TypeX[7,2] + TypeX[7,3] - TypeX[8,0] >= 0
 R66: - TypeX[7,2] - TypeX[7,3] + 2 TypeX[8,0] >= 0
 R67: TypeX[7,4] + TypeX[7,5] - TypeX[8,2] >= 0
 R68: - TypeX[7,4] - TypeX[7,5] + 2 TypeX[8,2] >= 0
 R69: TypeX[7,0] - TypeX[8,1] = 0
 R70: TypeX[7,2] - TypeX[8,3] = 0
 R71: TypeX[7,4] - TypeX[8,5] = 0
 R72: - TypeY[7,0] + TypeY[8,1] + TypeY[8,4] >= 0
 R73: 2 TypeY[7,0] - TypeY[8,1] - TypeY[8,4] >= 0
 R74: - TypeY[7,2] + TypeY[8,0] + TypeY[8,3] >= 0
 R75: 2 TypeY[7,2] - TypeY[8,0] - TypeY[8,3] >= 0
 R76: - TypeY[7,4] + TypeY[8,2] + TypeY[8,5] >= 0
 R77: 2 TypeY[7,4] - TypeY[8,2] - TypeY[8,5] >= 0
 R78: - TypeY[7,1] + TypeY[8,4] = 0
 R79: - TypeY[7,3] + TypeY[8,0] = 0
 R80: - TypeY[7,5] + TypeY[8,2] = 0
 R81: - TypeY[6,0] + TypeY[7,1] + TypeY[7,4] >= 0
 R82: 2 TypeY[6,0] - TypeY[7,1] - TypeY[7,4] >= 0
 R83: - TypeY[6,2] + TypeY[7,0] + TypeY[7,3] >= 0
 R84: 2 TypeY[6,2] - TypeY[7,0] - TypeY[7,3] >= 0
 R85: - TypeY[6,4] + TypeY[7,2] + TypeY[7,5] >= 0
 R86: 2 TypeY[6,4] - TypeY[7,2] - TypeY[7,5] >= 0
 R87: - TypeY[6,1] + TypeY[7,4] = 0
 R88: - TypeY[6,3] + TypeY[7,0] = 0
 R89: - TypeY[6,5] + TypeY[7,2] = 0
 R90: - TypeY[5,0] + TypeY[6,1] + TypeY[6,4] >= 0
 R91: 2 TypeY[5,0] - TypeY[6,1] - TypeY[6,4] >= 0
 R92: - TypeY[5,2] + TypeY[6,0] + TypeY[6,3] >= 0
 R93: 2 TypeY[5,2] - TypeY[6,0] - TypeY[6,3] >= 0
 R94: - TypeY[5,4] + TypeY[6,2] + TypeY[6,5] >= 0
 R95: 2 TypeY[5,4] - TypeY[6,2] - TypeY[6,5] >= 0
 R96: - TypeY[5,1] + TypeY[6,4] = 0
 R97: - TypeY[5,3] + TypeY[6,0] = 0
 R98: - TypeY[5,5] + TypeY[6,2] = 0
 R99: - TypeY[4,0] + TypeY[5,1] + TypeY[5,4] >= 0
 R100: 2 TypeY[4,0] - TypeY[5,1] - TypeY[5,4] >= 0
 R101: - TypeY[4,2] + TypeY[5,0] + TypeY[5,3] >= 0
 R102: 2 TypeY[4,2] - TypeY[5,0] - TypeY[5,3] >= 0
 R103: - TypeY[4,4] + TypeY[5,2] + TypeY[5,5] >= 0
 R104: 2 TypeY[4,4] - TypeY[5,2] - TypeY[5,5] >= 0
 R105: - TypeY[4,1] + TypeY[5,4] = 0
 R106: - TypeY[4,3] + TypeY[5,0] = 0
 R107: - TypeY[4,5] + TypeY[5,2] = 0
 R108: - TypeY[3,0] + TypeY[4,1] + TypeY[4,4] >= 0
 R109: 2 TypeY[3,0] - TypeY[4,1] - TypeY[4,4] >= 0
 R110: - TypeY[3,2] + TypeY[4,0] + TypeY[4,3] >= 0
 R111: 2 TypeY[3,2] - TypeY[4,0] - TypeY[4,3] >= 0
 R112: - TypeY[3,4] + TypeY[4,2] + TypeY[4,5] >= 0
 R113: 2 TypeY[3,4] - TypeY[4,2] - TypeY[4,5] >= 0
 R114: - TypeY[3,1] + TypeY[4,4] = 0
 R115: - TypeY[3,3] + TypeY[4,0] = 0
 R116: - TypeY[3,5] + TypeY[4,2] = 0
 R117: - TypeY[2,0] + TypeY[3,1] + TypeY[3,4] >= 0
 R118: 2 TypeY[2,0] - TypeY[3,1] - TypeY[3,4] >= 0
 R119: - TypeY[2,2] + TypeY[3,0] + TypeY[3,3] >= 0
 R120: 2 TypeY[2,2] - TypeY[3,0] - TypeY[3,3] >= 0
 R121: - TypeY[2,4] + TypeY[3,2] + TypeY[3,5] >= 0
 R122: 2 TypeY[2,4] - TypeY[3,2] - TypeY[3,5] >= 0
 R123: - TypeY[2,1] + TypeY[3,4] = 0
 R124: - TypeY[2,3] + TypeY[3,0] = 0
 R125: - TypeY[2,5] + TypeY[3,2] = 0
 R126: - TypeY[1,0] + TypeY[2,1] + TypeY[2,4] >= 0
 R127: 2 TypeY[1,0] - TypeY[2,1] - TypeY[2,4] >= 0
 R128: - TypeY[1,2] + TypeY[2,0] + TypeY[2,3] >= 0
 R129: 2 TypeY[1,2] - TypeY[2,0] - TypeY[2,3] >= 0
 R130: - TypeY[1,4] + TypeY[2,2] + TypeY[2,5] >= 0
 R131: 2 TypeY[1,4] - TypeY[2,2] - TypeY[2,5] >= 0
 R132: - TypeY[1,1] + TypeY[2,4] = 0
 R133: - TypeY[1,3] + TypeY[2,0] = 0
 R134: - TypeY[1,5] + TypeY[2,2] = 0
 R135: - TypeY[0,0] + TypeY[1,1] + TypeY[1,4] >= 0
 R136: 2 TypeY[0,0] - TypeY[1,1] - TypeY[1,4] >= 0
 R137: - TypeY[0,2] + TypeY[1,0] + TypeY[1,3] >= 0
 R138: 2 TypeY[0,2] - TypeY[1,0] - TypeY[1,3] >= 0
 R139: - TypeY[0,4] + TypeY[1,2] + TypeY[1,5] >= 0
 R140: 2 TypeY[0,4] - TypeY[1,2] - TypeY[1,5] >= 0
 R141: - TypeY[0,1] + TypeY[1,4] = 0
 R142: - TypeY[0,3] + TypeY[1,0] = 0
 R143: - TypeY[0,5] + TypeY[1,2] = 0
 R144: TypeX[0,0] - TypeZ[0,0] >= 0
 R145: TypeY[0,1] - TypeZ[0,0] >= 0
 R146: - TypeX[0,0] - TypeY[0,1] + TypeZ[0,0] >= -1
 R147: TypeX[0,2] - TypeZ[0,1] >= 0
 R148: TypeY[0,3] - TypeZ[0,1] >= 0
 R149: - TypeX[0,2] - TypeY[0,3] + TypeZ[0,1] >= -1
 R150: TypeX[0,4] - TypeZ[0,2] >= 0
 R151: TypeY[0,5] - TypeZ[0,2] >= 0
 R152: - TypeX[0,4] - TypeY[0,5] + TypeZ[0,2] >= -1
 R153: TypeX[1,0] - TypeZ[1,0] >= 0
 R154: TypeY[1,1] - TypeZ[1,0] >= 0
 R155: - TypeX[1,0] - TypeY[1,1] + TypeZ[1,0] >= -1
 R156: TypeX[1,2] - TypeZ[1,1] >= 0
 R157: TypeY[1,3] - TypeZ[1,1] >= 0
 R158: - TypeX[1,2] - TypeY[1,3] + TypeZ[1,1] >= -1
 R159: TypeX[1,4] - TypeZ[1,2] >= 0
 R160: TypeY[1,5] - TypeZ[1,2] >= 0
 R161: - TypeX[1,4] - TypeY[1,5] + TypeZ[1,2] >= -1
 R162: TypeX[2,0] - TypeZ[2,0] >= 0
 R163: TypeY[2,1] - TypeZ[2,0] >= 0
 R164: - TypeX[2,0] - TypeY[2,1] + TypeZ[2,0] >= -1
 R165: TypeX[2,2] - TypeZ[2,1] >= 0
 R166: TypeY[2,3] - TypeZ[2,1] >= 0
 R167: - TypeX[2,2] - TypeY[2,3] + TypeZ[2,1] >= -1
 R168: TypeX[2,4] - TypeZ[2,2] >= 0
 R169: TypeY[2,5] - TypeZ[2,2] >= 0
 R170: - TypeX[2,4] - TypeY[2,5] + TypeZ[2,2] >= -1
 R171: TypeX[3,0] - TypeZ[3,0] >= 0
 R172: TypeY[3,1] - TypeZ[3,0] >= 0
 R173: - TypeX[3,0] - TypeY[3,1] + TypeZ[3,0] >= -1
 R174: TypeX[3,2] - TypeZ[3,1] >= 0
 R175: TypeY[3,3] - TypeZ[3,1] >= 0
 R176: - TypeX[3,2] - TypeY[3,3] + TypeZ[3,1] >= -1
 R177: TypeX[3,4] - TypeZ[3,2] >= 0
 R178: TypeY[3,5] - TypeZ[3,2] >= 0
 R179: - TypeX[3,4] - TypeY[3,5] + TypeZ[3,2] >= -1
 R180: TypeX[4,0] - TypeZ[4,0] >= 0
 R181: TypeY[4,1] - TypeZ[4,0] >= 0
 R182: - TypeX[4,0] - TypeY[4,1] + TypeZ[4,0] >= -1
 R183: TypeX[4,2] - TypeZ[4,1] >= 0
 R184: TypeY[4,3] - TypeZ[4,1] >= 0
 R185: - TypeX[4,2] - TypeY[4,3] + TypeZ[4,1] >= -1
 R186: TypeX[4,4] - TypeZ[4,2] >= 0
 R187: TypeY[4,5] - TypeZ[4,2] >= 0
 R188: - TypeX[4,4] - TypeY[4,5] + TypeZ[4,2] >= -1
 R189: TypeX[5,0] - TypeZ[5,0] >= 0
 R190: TypeY[5,1] - TypeZ[5,0] >= 0
 R191: - TypeX[5,0] - TypeY[5,1] + TypeZ[5,0] >= -1
 R192: TypeX[5,2] - TypeZ[5,1] >= 0
 R193: TypeY[5,3] - TypeZ[5,1] >= 0
 R194: - TypeX[5,2] - TypeY[5,3] + TypeZ[5,1] >= -1
 R195: TypeX[5,4] - TypeZ[5,2] >= 0
 R196: TypeY[5,5] - TypeZ[5,2] >= 0
 R197: - TypeX[5,4] - TypeY[5,5] + TypeZ[5,2] >= -1
 R198: TypeX[6,0] - TypeZ[6,0] >= 0
 R199: TypeY[6,1] - TypeZ[6,0] >= 0
 R200: - TypeX[6,0] - TypeY[6,1] + TypeZ[6,0] >= -1
 R201: TypeX[6,2] - TypeZ[6,1] >= 0
 R202: TypeY[6,3] - TypeZ[6,1] >= 0
 R203: - TypeX[6,2] - TypeY[6,3] + TypeZ[6,1] >= -1
 R204: TypeX[6,4] - TypeZ[6,2] >= 0
 R205: TypeY[6,5] - TypeZ[6,2] >= 0
 R206: - TypeX[6,4] - TypeY[6,5] + TypeZ[6,2] >= -1
 R207: TypeX[7,0] - TypeZ[7,0] >= 0
 R208: TypeY[7,1] - TypeZ[7,0] >= 0
 R209: - TypeX[7,0] - TypeY[7,1] + TypeZ[7,0] >= -1
 R210: TypeX[7,2] - TypeZ[7,1] >= 0
 R211: TypeY[7,3] - TypeZ[7,1] >= 0
 R212: - TypeX[7,2] - TypeY[7,3] + TypeZ[7,1] >= -1
 R213: TypeX[7,4] - TypeZ[7,2] >= 0
 R214: TypeY[7,5] - TypeZ[7,2] >= 0
 R215: - TypeX[7,4] - TypeY[7,5] + TypeZ[7,2] >= -1
 R216: TypeX[0,0] + TypeX[0,1] + TypeX[0,2] + TypeX[0,3] + TypeX[0,4]
   + TypeX[0,5] >= 1
 R217: TypeY[8,0] + TypeY[8,1] + TypeY[8,2] + TypeY[8,3] + TypeY[8,4]
   + TypeY[8,5] >= 1
 R218: TypeZ[0,0] + TypeZ[0,1] + TypeZ[0,2] + TypeZ[1,0] + TypeZ[1,1]
   + TypeZ[1,2] + TypeZ[2,0] + TypeZ[2,1] + TypeZ[2,2] + TypeZ[3,0]
   + TypeZ[3,1] + TypeZ[3,2] + TypeZ[4,0] + TypeZ[4,1] + TypeZ[4,2]
   + TypeZ[5,0] + TypeZ[5,1] + TypeZ[5,2] + TypeZ[6,0] + TypeZ[6,1]
   + TypeZ[6,2] + TypeZ[7,0] + TypeZ[7,1] + TypeZ[7,2] <= 5
Bounds
Binaries
 TypeX[0,0] TypeX[0,1] TypeX[0,2] TypeX[0,3] TypeX[0,4] TypeX[0,5]
 TypeX[1,0] TypeX[1,1] TypeX[1,2] TypeX[1,3] TypeX[1,4] TypeX[1,5]
 TypeX[2,0] TypeX[2,1] TypeX[2,2] TypeX[2,3] TypeX[2,4] TypeX[2,5]
 TypeX[3,0] TypeX[3,1] TypeX[3,2] TypeX[3,3] TypeX[3,4] TypeX[3,5]
 TypeX[4,0] TypeX[4,1] TypeX[4,2] TypeX[4,3] TypeX[4,4] TypeX[4,5]
 TypeX[5,0] TypeX[5,1] TypeX[5,2] TypeX[5,3] TypeX[5,4] TypeX[5,5]
 TypeX[6,0] TypeX[6,1] TypeX[6,2] TypeX[6,3] TypeX[6,4] TypeX[6,5]
 TypeX[7,0] TypeX[7,1] TypeX[7,2] TypeX[7,3] TypeX[7,4] TypeX[7,5]
 TypeX[8,0] TypeX[8,1] TypeX[8,2] TypeX[8,3] TypeX[8,4] TypeX[8,5]
 TypeY[0,0] TypeY[0,1] TypeY[0,2] TypeY[0,3] TypeY[0,4] TypeY[0,5]
 TypeY[1,0] TypeY[1,1] TypeY[1,2] TypeY[1,3] TypeY[1,4] TypeY[1,5]
 TypeY[2,0] TypeY[2,1] TypeY[2,2] TypeY[2,3] TypeY[2,4] TypeY[2,5]
 TypeY[3,0] TypeY[3,1] TypeY[3,2] TypeY[3,3] TypeY[3,4] TypeY[3,5]
 TypeY[4,0] TypeY[4,1] TypeY[4,2] TypeY[4,3] TypeY[4,4] TypeY[4,5]
 TypeY[5,0] TypeY[5,1] TypeY[5,2] TypeY[5,3] TypeY[5,4] TypeY[5,5]
 TypeY[6,0] TypeY[6,1] TypeY[6,2] TypeY[6,3] TypeY[6,4] TypeY[6,5]
 TypeY[7,0] TypeY[7,1] TypeY[7,2] TypeY[7,3] TypeY[7,4] TypeY[7,5]
 TypeY[8,0] TypeY[8,1] TypeY[8,2] TypeY[8,3] TypeY[8,4] TypeY[8,5]
 TypeZ[0,0] TypeZ[0,1] TypeZ[0,2] TypeZ[1,0] TypeZ[1,1] TypeZ[1,2]
 TypeZ[2,0] TypeZ[2,1] TypeZ[2,2] TypeZ[3,0] TypeZ[3,1] TypeZ[3,2]
 TypeZ[4,0] TypeZ[4,1] TypeZ[4,2] TypeZ[5,0] TypeZ[5,1] TypeZ[5,2]
 TypeZ[6,0] TypeZ[6,1] TypeZ[6,2] TypeZ[7,0] TypeZ[7,1] TypeZ[7,2]
End
