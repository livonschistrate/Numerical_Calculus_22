from cmath import pi
import numpy as np
from math import sin, cos

def ex1(final):
    
    if final == "show":
        print("**********")
    
    m = 0
    while 10**(-m) + 1.0 != 1.0:
        m += 1
    m-=1
        
    if final == "show":
        print("Precizia masina este: ", 10**(-m))
        print("**********")
    elif final == "return":
        return 10**(-m)
    
    
def ex2():
    
    print("**********")
    
    u = ex1("return")
    a = 1.0
    b = u/10
    c = b
    if (a+b)+c == a+(b+c):
        print("Obtinem adunare asociativa.")
    else:
        print("Obtinem adunare neasociativa.")
        
    a,b = u,1.25
    c = b
    if (a*b)*c == a*(b*c):
        print("Obtinem inmultire asociativa.")
    else:
        print("Obtinem inmultire neasociativa.")

    print("**********")
    
    
def ex3(x):
    
    z = (x-1)/(x+1)
    
    sina = [1805490264.690988571178600370234394843221,  
       -164384678.227499837726129612587952660511,  
       3664210.647581261810227924465160827365,  
       -28904.140246461781357223741935980097,  
       76.568981088717405810132543523682]
    
    sinb = [2298821602.638922662086487520330827251172, 
       27037050.118894436776624866648235591988,  
       155791.388546947693206469423979505671, 
       540.567501261284024767779280700089, 
       1.0 ]
    
    cosa = [1090157078.174871420428849017262549038606, 
       -321324810.993150712401352959397648541681,  
        12787876.849523878944051885325593878177, 
        -150026.206045948110568310887166405972, 
       538.333564203182661664319151379451  ]
    
    cosb = [1090157078.174871420428867295670039506886,  
        14907035.776643879767410969509628406502,  
       101855.811943661368302608146695082218, 
       429.772865107391823245671264489311,  
       1.0]
    
    lna = [75.151856149910794642732375452928,  
        -134.730399688659339844586721162914, 
        74.201101420634257326499008275515, 
        -12.777143401490740103758406454323, 
        0.332579601824389206151063529971]
    
    lnb = [37.575928074955397321366156007781, 
       -79.890509202648135695909995521310,  
       56.215534829542094277143417404711, 
       -14.516971195056682948719125661717, 
       1.0]
    
    p4_sin,q4_sin = 0,0
    p4_cos,q4_cos = 0,0
    p4_ln,q4_ln = 0,0
    
    for i in reversed(range(len(sina))):
        if i:
            p4_sin = x*x*(p4_sin + sina[i])
            q4_sin = x*x*(q4_sin + sinb[i])
            p4_cos = x*x*(p4_cos + cosa[i])
            q4_cos = x*x*(q4_cos + cosb[i])
            p4_ln = z*z*(p4_ln + lna[i])
            q4_ln = z*z*(q4_ln + lnb[i])
        else:
            p4_sin = p4_sin + sina[i]
            q4_sin = q4_sin + sinb[i]
            p4_cos = p4_cos + cosa[i]
            q4_cos = q4_cos + cosb[i]
            p4_ln = p4_ln + lna[i]
            q4_ln = q4_ln + lnb[i]
            
    aprox_sin = x*p4_sin/q4_sin
    aprox_cos = p4_cos/q4_cos
    aprox_ln = z*p4_ln/q4_ln
    
    r_sin = aprox_sin/sin(.25*pi*x)
    r_cos = aprox_cos/cos(.25*pi*x)
    r_ln = aprox_ln/np.log(x)
    
    
    print("**********")
    print("Obtinem valorile:")
    print("Pentru sinus: ", aprox_sin, sin(.25*pi*x))
    print("Pentru cosinus: ", aprox_cos, cos(.25*pi*x))
    print("Pentru logaritm: ", aprox_ln, np.log(x))
    
    
    print("Comparatii:")
    print("Pentru sinus: ", r_sin)
    print("Pentru cosinus: ", r_cos)
    print("Pentru logaritm: ", r_ln)
    print("**********")
    
while(1):
    print("Alege exercitiul:")
    ex_number = input()
    if ex_number == '1':
        ex1("show")
    elif ex_number == '2':
        ex2()
    elif ex_number == '3':
        ex3(0.45)
    elif ex_number == 'q':
        print("Se iese din aplicatie.")
        break
    else:
        print("Numar gresit.")