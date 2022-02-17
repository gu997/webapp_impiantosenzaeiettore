from flask import Flask, request, render_template#, redirect#, url_for
import base64
from io import BytesIO
#from matplotlib.figure import Figure
#import os
import grafici_termodinamici_tkinter as gt
from CoolProp.CoolProp import PropsSI
import numpy as np
import compressore as c

#UPLOAD_FOLDER = 'static/img/'

app = Flask(__name__)

#picFolder = os.path.join('static', 'img')
#print(picFolder)
#app.config['UPLOAD_FOLDER'] = picFolder
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



# =============================================================================
# @app.route('/ph')
# def PH():
# # =============================================================================
# #     P_gc = request.args.get('P_gc', None)
# #     P_gc = request.args.get('P_gc', None)
# #     P_gc = request.args.get('P_gc', None)
# #     P_gc = request.args.get('P_gc', None)
# #     P_gc = request.args.get('P_gc', None)
# # =============================================================================
#     #return render_template('image_PH.html',plot_url=data)
#     return 'jgjfkdktyd'
# =============================================================================

@app.route('/', methods=['POST', 'GET'])
def response():
    
    pic1 =1# os.path.join(app.config['UPLOAD_FOLDER'], 'impianto_senza_eiettore.png')
    pic2 =2# os.path.join(app.config['UPLOAD_FOLDER'], 'ThermoGroup_Logo_NonAnimato.png')
    
    if request.method == "POST":
        P_gc = request.form.get("P_gc")
        T_gc = request.form.get("T_gc")
        T_eva = request.form.get("T_eva")
        T_sep = request.form.get("T_sep")
        eps = request.form.get("eps")
        
        P_gc=float(P_gc)
        T_gc=float(T_gc)
        T_eva=float(T_eva)
        T_sep=float(T_sep)
        eps=float(eps)


        
        T=np.zeros(11)
        P=np.zeros(11)
        H=np.zeros(11)
        S=np.zeros(11)
        m=np.ones(3)
    
        T_ref=273.15
    
        "PUNTI NOTI A PRIORI"
    
        T[3]=T_gc+T_ref
        P[3]=P_gc*10**5   #iperparametro
        H[3]=PropsSI('H','T',T[3],'P',P[3],'CO2')
    
        T[8]=T_eva+T_ref
        P[8]=PropsSI('P','T',T[8],'Q',1,'CO2')
        H[8]=PropsSI('H','T',T[8],'Q',1,'CO2')
    
        P[0]=P[8]
        T[0]=T[8]
            
        T[5]=T_sep+T_ref 
        P[5]=PropsSI('P','Q',0,'T',T[5],'CO2')
    
        P[9]=P[5]
        T[9]=T[5]
        H[9]=PropsSI('H','T',T[5],'Q',1,'CO2')
    
        P[6]=P[5]
        T[6]=T[5]
        H[6]=PropsSI('H','T',T[5],'Q',0,'CO2')
    
        H[7]=H[6]
        P[7]=P[8]
        T[7]=PropsSI('T','H',H[7],'P',P[7],'CO2')
           
        H[10]=H[9]
        P[10]=P[8]
        T[10]=PropsSI('T','H',H[10],'P',P[10],'CO2')
        
        T[1]=T[0] + eps*(T[3]-T[0])
        P[1]=P[0]
        H[1]=PropsSI('H','T',T[1],'P',P[1],'CO2')
        
        "IPOTIZZO IL PUNTO 0"
        
        Q0_0=0.98973511
        Q0=5
        for i in range(100):
            if abs(Q0-Q0_0)> 1e-05:
            
                Q0=Q0_0
                H[0]=PropsSI('H','T',T[0],'Q',Q0,'CO2')
                        
                 
                
                
                H[4]=H[3]-H[1]+H[0]
                P[4]=P[3]
                T[4]=PropsSI('T','H',H[4],'P',P[4],'CO2')
                S[4]=PropsSI('S','H',H[4],'P',P[4],'CO2')
                
                
                
                H[5]=H[4]
                Q=PropsSI('Q','H',H[5],'P',P[5],'CO2')
                
                m[1]=m[0]*(1-Q)
                m[2]=m[0]*Q
                
                H[0]=(m[1]*H[8]+m[2]*H[10])/m[0]
                Q0_0=PropsSI('Q','H',H[0],'P',P[0],'CO2')
                #print('Q0=',Q0_0)
           
            else:
                break
            
            
            
            
            
        
        "PUNTI RIMANENTI"
        m[0]=c.Portata(T[0]-T_ref, T[1]-T_ref, P[3]*10**-5)
        m[1]=m[0]*(1-Q)
        m[2]=m[0]*Q
        m=m/3600
        T[2]=c.Temperatura_mandata(T[0]-T_ref, T[1]-T_ref, P[3]*10**-5)+T_ref
        P[2]=P[3]
        H[2]=PropsSI('H','T',T[2],'P',P[2],'CO2')
        
        cop=(H[1]-H[3])/(H[2]-H[1])
        
        
        
        
        P=P*10**-5
        H=H*10**-3
        
        
        
        
        cop=(H[1]-H[3])/(H[2]-H[1])
        cop=round(cop, 2)
        W_cg=round(m[0]*(H[2]-H[3]), 2)
        W_eva=round(m[1]*(H[8]-H[7]), 2)
        W_IHX=round(m[0]*(H[3]-H[4]), 2)
        W_c=round(m[0]*(H[2]-H[1]), 2)
        
        
        P=np.round(P,1)
        T=np.round(T-T_ref,2)
        H=np.round(H,1)
        m=np.round(m,3)


        if request.form.get('submit_button') == 'grafico':
            # pass
            print("Encrypted")
            # Generate the figure **without using pyplot**.
# =============================================================================
#             fig = Figure(dpi=200)
#             ax = fig.subplots()
#             ax.plot([1, 2])
# =============================================================================
            # Save it to a temporary buffer.
            fig=gt.grafico_PH_sep(P,H)  
            buf = BytesIO()
            fig.savefig(buf, format="png")
            # Embed the result in the html output.
            data = base64.b64encode(buf.getbuffer()).decode("ascii")
            
            #print('\n\n\n',data)
            
            #return f"<img src='data:image/png;base64,{data}'/>"
            #return redirect(url_for('ph', data=data))
            #return redirect(url_for('ph'))
            return render_template('image_imp.html', P_gc=P_gc, T_gc=T_gc, T_eva=T_eva, T_sep=T_sep, eps=eps , user_image=pic1, user_image2=pic2, cop=cop, W_cg=W_cg, W_eva=W_eva, W_IHX=W_IHX, W_c=W_c,
                               P0=P[0],P1=P[1],P2=P[2],P3=P[3],P4=P[4],P5=P[5],P6=P[6],P7=P[7],P8=P[8],P9=P[9],P10=P[10],
                               T0=T[0],T1=T[1],T2=T[2],T3=T[3],T4=T[4],T5=T[5],T6=T[6],T7=T[7],T8=T[8],T9=T[9],T10=T[10],
                               H0=H[0],H1=H[1],H2=H[2],H3=H[3],H4=H[4],H5=H[5],H6=H[6],H7=H[7],H8=H[8],H9=H[9],H10=H[10],
                               m0=m[0],m1=m[1],m2=m[2], plot_url=data)
            
            
        return render_template('image_imp.html', P_gc=P_gc, T_gc=T_gc, T_eva=T_eva, T_sep=T_sep, eps=eps , user_image=pic1, user_image2=pic2, cop=cop, W_cg=W_cg, W_eva=W_eva, W_IHX=W_IHX, W_c=W_c,
                               P0=P[0],P1=P[1],P2=P[2],P3=P[3],P4=P[4],P5=P[5],P6=P[6],P7=P[7],P8=P[8],P9=P[9],P10=P[10],
                               T0=T[0],T1=T[1],T2=T[2],T3=T[3],T4=T[4],T5=T[5],T6=T[6],T7=T[7],T8=T[8],T9=T[9],T10=T[10],
                               H0=H[0],H1=H[1],H2=H[2],H3=H[3],H4=H[4],H5=H[5],H6=H[6],H7=H[7],H8=H[8],H9=H[9],H10=H[10],
                               m0=m[0],m1=m[1],m2=m[2])


    elif request.method == 'GET':  
        
        
        return render_template('image_imp.html', P_gc=95, T_gc=40, T_eva=-5, T_sep=5, eps=0.8 , user_image=pic1, user_image2=pic2) 

# =============================================================================
# 
# @app.route("/")
# def index():
#     pic1 = os.path.join(app.config['UPLOAD_FOLDER'], 'impianto_senza_eiettore.png')
#     pic2 = os.path.join(app.config['UPLOAD_FOLDER'], 'ThermoGroup_Logo_NonAnimato.png')
#     return render_template("image_imp.html", user_image=pic1, user_image2=pic2)   
# =============================================================================


if __name__ == '__main__':
    app.run()