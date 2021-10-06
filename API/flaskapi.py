import numpy as np
from numpy.lib.shape_base import column_stack
import pandas as pd
import matplotlib as mpl
from pandas.core.frame import DataFrame
mpl.use('tkagg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import *
from matplotlib import cm
import scipy as sp
from scipy.interpolate import griddata
from flask import Flask, json, request, jsonify
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS, cross_origin
import pandas as pd
import ast

#companies = [{"id": 1, "name": "Company One"}, {"id": 2, "name": "Company Two"}]
 
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app)


class Data(Resource):
    def emiss_comp(self,C,W,T,Tau,theta):
        Wt = 0.0286+0.00307*C
        nd = 1.634-0.00539*C+2.75*10**-5*C**2
        kd = 0.0395-4.038*10**-4*C

        nb = (8.86+0.00321*T)+(-0.0644+7.96*10**-4*T)*C+(2.97*10**-4-9.6*10**-6*T)*C**2
        kb = (0.738-0.00903*T+8.57*10**-5*T**2)+(-0.00215+1.47*10**-4*T)*C+(7.36*10**-5-1.03*10**-6*T+1.05*10**-8*T**2)*C**2
        nu = (10.3-0.0173*T)+(6.5*10**-4+8.82*10**-5*T)*C+(-6.34*10**-6-6.32*10**-7*T)*C**2
        ku = (0.7-0.017*T+1.78*10**-4*T**2)+(0.0161+7.25*10**-4*T)*C+(-1.46*10**-4-6.03*10**-6*T-7.87*10**-9*T**2)*C**2

        ns = 0
        if (W<=Wt):
            ns = nd+(nb-1)*W
        else:
            ns = nd+(nb-1)*Wt + (nu-1)*(W-Wt)

        ks = 0
        if (W<=Wt):
            ks = kd+kb*W
        else:
            ks = kd+kb*Wt + ku*(W-Wt)

        eps1 = ns**2-ks**2
        eps2 = 2*ns*ks


        eps = complex(eps1,eps2)
        
        theta = np.radians(theta) #theta in rad

        rH = np.abs((np.cos(theta)-np.sqrt(eps-np.sin(theta)**2))/(np.cos(theta)+np.sqrt(eps-np.sin(theta)**2)))**2
        rV = np.abs((eps*np.cos(theta)-np.sqrt(eps-np.sin(theta)**2))/(eps*np.cos(theta)+np.sqrt(eps-np.sin(theta)**2)))**2

        eH = 1-rH
        eV = 1-rV

        TsEh = (T+273.15)*eH
        TsEv = (T+273.15)*eV

        StransH = TsEh*np.exp(-Tau/np.cos(theta))
        StransV = TsEv*np.exp(-Tau/np.cos(theta))
        
        return T,W,Tau,eH,eV,StransH,StransV,TsEh,TsEv

    def compute_and_return_DF(self,C,theta,Tmax,Wmax):
        df = pd.DataFrame(columns=['T','W','Tau','eH','eV','StransH','StransV','TsEh','TsEv'])

        List_T = []
        List_W = []
        
        for W in np.arange(0, float(Wmax)+0.02, 0.02):
            for T in np.arange(0,int(Tmax)+2,2):
                List_T.append(T)
                List_W.append(W)


        df['T'] = List_T
        df['W'] = List_W

        List_Tau = []
        List_rH = []
        List_rV = []
        List_StransH = []
        List_StransV = []
        List_TsEh = []
        List_TsEv = []
        for idx in df.index:
            T,W,Tau,rH,rV,StransH,StransV,TsEh,TsEv = self.emiss_comp(C,df['W'][idx],df['T'][idx],0,theta)  #set Tau = 0 cause physical test doesnt need Tau
            List_T.append(T)
            List_W.append(W)
            List_Tau.append(Tau)
            List_rH.append(rH)
            List_rV.append(rV)
            List_StransH.append(StransH)
            List_StransV.append(StransV)
            List_TsEh.append(TsEh)
            List_TsEv.append(TsEv)

        df['Tau'] = List_Tau
        df['eH'] = List_rH
        df['eV'] = List_rV
        df['StransH'] = List_StransH
        df['StransV'] = List_StransV
        df['TsEh'] = List_TsEh
        df['TsEv'] = List_TsEv

        x = df['W'].tolist()
        y = df['T'].tolist()
        z = df['TsEh'].tolist()

        xi = np.linspace(min(x),max(x))
        yi = np.linspace(min(y),max(y))
        X, Y = np.meshgrid(xi, yi)
        points = np.column_stack((x,y))
        Z = griddata(points, z, (X, Y), method='linear')
        #print(xi)
        #print(yi)
        df2 = pd.DataFrame(Z,index=xi,columns=yi)
        return df,xi,yi,Z
    
    def post(self):
        content = request.get_json()
        C = int(content['C'])
        theta = int(content['theta'])
        Tmax = int(content['Tmax'])
        Wmax = float(content['Wmax'])

        df,X,Y,Z = self.compute_and_return_DF(C,theta,Tmax,Wmax)
        df.to_csv('data.csv',index=False)
        x_json = json.dumps(X.tolist())
        y_json = json.dumps(Y.tolist())
        z_json = json.dumps(Z.tolist())
        #print(z_json)
        #df2.to_csv('data2.csv',index=False)
        return {'x_data':x_json,'y_data':y_json,'z_data':z_json}, 200
        #return jsonify(x_data=x_json,y_data=y_json,z_data=z_json),200

#@api.route('/companies', methods=['POST'])
#def post_companies():
#  return json.dumps({"success":True}), 201
api.add_resource(Data, '/data')  # add endpoints


if __name__ == '__main__':
    app.run() 