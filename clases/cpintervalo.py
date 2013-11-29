from intervalo import *

import numpy as np

math=np

class CPIntervalo(object):
    '''
    Clase auxiliar en la construccion de intervalos complejos en coordenadas
    polares
    '''
    
    def __init__(self, mod, arg=None):
        
        '''
        Se define el intervalo complejo a partir de los modulos y las fases, la primera
        entrada corresponde al intervalo del modulo y el segundo al del argumento
        '''
        
        #Si la entrada del argumento es nula el intervalo se toma como real
        
        if not isinstance(mod,Intervalo):
            
            mod=Intervalo(mod)
            
        
        if arg is None:
            
            if mod.lo<0 and mod.hi<=0:
            
                arg = Intervalo(math.pi)
                
                
            if mod.lo<0 and mod.hi>0:
                
                arg=Intervalo(0.0, math.pi)
                
            
            if mod.lo>=0 and mod.hi>=0:
                
                arg=Intervalo(0.0)
                
            mod=Intervalo(math.sign(mod.lo)*mod.lo, math.sign(mod.hi)*mod.hi)
            
        
            
        if mod.lo<0 and mod.hi>=0:
            
            mod.lo=0
            
            print 'El radio no puede ser cero, el limite inferior se tomo como r=0'
        
        if mod.lo < 0 and mod.hi < 0:
            
            print 'El radio es completamente negativo'
            
            return None
            
        if not isinstance(arg,Intervalo):
            
            arg=Intervalo(arg)
            
        #arg=module(arg, 2*math.pi)
            
        
        
        self.mod = mod
        #self.arg = math.mod(arg, 2*math.pi)
        self.arg = arg
        
        
    def __repr__(self):
        return "CPIntervalo [{},{}]".format(self.mod,self.arg)
    
    def __str__(self):
        return "[{},{}]_p".format(self.mod,self.arg)

    def _repr_html_(self):
        reprn = "[{}, {}]<sub>p</sub>".format(self.mod, self.arg)
        reprn = reprn.replace("inf", r"&infin;")
        return reprn
    
    def _repr_latex_(self):
        return "$[{}, {}]_p$".format(self.mod, self.arg)
    
    def __mul__(self,otro):
        
        if not isinstance(otro, CPIntervalo):
            
            otro=CPIntervalo(otro)
        
        return CPIntervalo(self.mod*otro.mod,self.arg+otro.arg)
        
    def __rmul__(self, otro):
        
        return self*otro
        
    def __radd__(self, otro):
        
        return self+otro
        
    def __rsub__(self, otro):
        
        return self-otro
        
    def __rdiv__(self,otro):
        
        if not isinstance(otro, CPIntervalo):
            
            otro=CPIntervalo(otro)
            
        return CPIntervalo.__div__(otro, self)
        
    
    def __add__(self,otro):
        
        if not isinstance(otro,CPIntervalo):
            
            otro=CPIntervalo(otro)
        
        
        valreal=self.mod*cos(self.arg)+otro.mod*cos(otro.arg)
              
        valimag=self.mod*sin(self.arg)+otro.mod*sin(otro.arg)
        
        return CPIntervalo(sqrt(valreal**2+valimag**2),arctan(valimag/valreal))
        
    def __contains__(self, otro):
        
        '''
        Se inclu
        '''
        
        if not isinstance(otro, CPIntervalo):
            
            otro=CPIntervalo(otro)

        if otro.mod==0:
            
            return otro.mod & self.mod == otro.mod
            
        return otro & self == otro 
        
    def conjugate(self):
        
        '''
        Calcula el complejo conjugado
        '''
        
        return CPIntervalo(self.mod, -self.arg)
        
        
    def __eq__(self, otro):
        """
        funcion igualdad para intervalos 
        """
        if self.arg == otro.arg:
            
            return self.mod == otro.mod
            
        return False
                
    
    def __neg__(self):
        
        return CPIntervalo(self.mod,self.arg+math.pi)
    
    def __sub__(self,otro):
        
        if not isinstance(otro,CPIntervalo):
            
            otro=CPIntervalo(otro)
        
        valreal=self.mod*cos(self.arg)-otro.mod*cos(otro.arg)
              
        valimag=self.mod*sin(self.arg)-otro.mod*sin(otro.arg)
        
        return CPIntervalo(sqrt(valreal**2+valimag**2),arctan(valimag/valreal))
        
    def __div__(self,otro):
        
        if not isinstance(otro, CPIntervalo):
            
            otro=CPIntervalo(otro)
        
        return CPIntervalo(self.mod/otro.mod,self.arg-otro.arg)
        
    def reciprocal(self):
        
        if 0 in self:
            #si el intervalo contiene el cero debe de aparecer un error
            raise ZeroDivisionError
        else:
            return CPIntervalo(1.0/self.mod, -self.arg)
        
        
    def log(self):
        
        modul=sqrt(log(self.mod)**2+self.arg**2)
        
        argumento=arctan(self.arg/(log(self.mod)))
        
        return CPIntervalo(modul, argumento)
        
        
    def exp(self):
        
        return CPIntervalo(exp(self.mod*cos(self.arg)), self.mod*sin(self.arg))
        
    def __pow__(self, otro):
        
        if not isinstance(otro, CPIntervalo):
            
            otro=CPIntervalo(otro)
        
        aux=log(self)        
        
        return exp(otro*aux)
        
    def __rpow__(self, otro):
        
        if not isinstance(otro, CPIntervalo):
            
            otro=CPIntervalo(otro)
            
        return otro**self
        
        
    def __and__(self, otro):
        
        if not isinstance(otro, CPIntervalo):
            otro = CPIntervalo(otro)
            
        if self.mod & otro.mod== None:
            
            return None
            
        if self.arg & otro.arg == None:
            
            return None
            
        return CPIntervalo(self.mod & otro.mod, self.arg & otro.arg)
        
        
        
    def sqrt(self):
        
        return CPIntervalo(math.sqrt(self.mod), self.arg/2)
        
        
        
    def middle(self):
        
        
        return CPIntervalo(self.mod.middle(), self.arg.middle())
        
    #El seno y el coseno ya dan los valores bien por lo menos para intervalos
    #degenerados, lo demas depende si estan bien definidas las operaciones
    #en la clase intervalo        
        
    def cos(self):
        
        caux=self.mod*cos(self.arg)
        
        saux=self.mod*sin(self.arg)
        
        return (exp(CPIntervalo(-saux))*CPIntervalo(1.0, caux)+\
        
        exp(CPIntervalo(saux))*CPIntervalo(1.0,-caux))*0.5
        
    def sin(self):
        
        return cos(self-CPIntervalo(math.pi*0.5))
    
    def tan(self):
        
        return sin(self)/cos(self)
        
#funciones elementales para intervalos, para que funcionen cosas tipo funcion(a)
def exp(x):
    try:
        return x.exp()
    except:
        return math.exp(x)

def log(x):
    try:
        return x.log()
    except:
        return math.log(x)

def sqrt(x):
    try:
        return x.sqrt()
    except:
        return math.sqrt(x)
        