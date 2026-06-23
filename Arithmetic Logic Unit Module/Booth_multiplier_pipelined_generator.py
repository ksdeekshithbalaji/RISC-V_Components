k = ''  # initialize global string

def start(b):
    global k
    bb = b - 1
    temp = (2 * b) - 1
    t = temp + 1
    u = b * '0'
    k += f"module Multiplier_{b}_self(x, y, clk, q, reset);\n\n"
    k += f'''
input  signed [{bb}:0] x, y;
input  clk;
output reg signed [{temp}:0] q;

reg  signed [{t}:0] p [{bb}:0];
wire signed [{t}:0] p_init;
wire signed [{t}:0] a, s;
assign a      = {{x, 4'b{u}, 1'b0}};      // +multiplicand
assign s      = {{-x, 4'b{u}, 1'b0}};     // -multiplicand
assign p_init = {{4'b{u}, y, 1'b0}};      // multiplier
'''
    
def startloop():
    global k
    k+="\n"
    k+=f'''
// Stage 1
always @(posedge clk)
begin
    case(p_init[1:0])
        2'b01: p[0] <= (p_init + a) >>> 1;
        2'b10: p[0] <= (p_init + s) >>> 1;
        default: p[0] <= p_init >>> 1;
    endcase
end
'''

def midloop(b,i):
    global k
    k+='\n'
    db=i-2
    sb=i-1
    k+=f'''
// Stage {i}
always @(posedge clk)
begin
    case(p[{db}][1:0])
        2'b01: p[{sb}] <= (p[{db}] + a) >>> 1;
        2'b10: p[{sb}] <= (p[{db}] + s) >>> 1;
        default: p[{sb}] <= p[{db}] >>> 1;
    endcase
end
'''
def endloop(b,i):
    global k
    k+='\n'
    db=i-2
    sb=i-1
    tt=2*b
    k+=f'''
// Stage {i}
always @(posedge clk)
begin
    case(p[{db}][1:0])
        2'b01: p[{sb}] <= (p[{db}] + a) >>> 1;
        2'b10: p[{sb}] <= (p[{db}] + s) >>> 1;
        default: p[{sb}] <= p[{db}] >>> 1;
    endcase

    q <= p[{sb}][{tt}:1];
end

endmodule
'''

z=int(input("ENTER THE NUMBER OF BIT ="))
start(z)
startloop()
for i in range(2,z):
    midloop(z,i)

endloop(z,z)

f=open(f"Multiplier_{z}_bit_booth_p",'w')
f.write(k)
f.close()
print(f"SUCCESSFULL CREATED AND SAVED 'Multiplier_{z}_bit_booth_p'")
