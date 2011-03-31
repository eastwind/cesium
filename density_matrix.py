#!/usr/bin/python2
from __future__ import division
import numpy as np
from progress_bar import ProgressBar
import sys

class System:
    """
    """
    def density_length(self,n):
        """
        Calculate number of independant variable in the density matrix.
        """
        return n+(n*(n-1)) #n+2(n-1+1)(n-1)/2 because non diagonal terms are complex

    def hamiltonian(self,i,j):
        if i==j:
            return self.omega[i]
        else:
            return self.dipole[i][j]

    def density_index(self,i,j):
        if j<i:
            raise IOError('only upper diagonal part')
        if i==j:
            return (self.n+(self.n-i+1))*i-i
        else:
            return (self.n+(self.n-i+1))*i-i+(j-i)*2-1

    def normalize(self,matrix):
        """
        No need to calculate bloch equation of rho_nn.
        rho_11+rho_22....rho_nn = 1
        """
        for i in range(self.n):
            matrix[self.N-1][self.density_index(i,i)]=1
        return matrix

    def same_group(self,i,j):
        """
        If levels are in same group?
        """
        for g in self.groups:
            if (i in g) and (j in g):
                return True
        else:
            return False

    def interaction_freq(self,i,j):
        if self.same_group(i,j):
            return 0
        else:
            if (i in self.up) and (j in self.low1):
                return -1*self.nu[0]
            elif ((i in self.up) and (j in self.low2)):
                return -1*self.nu[1]
            elif ((i in self.low1) and (j in self.low2)):
                return self.nu[0]-self.nu[1]
            elif (j in self.up) and (i in self.low1):
                return self.nu[0]
            elif ((j in self.up) and (i in self.low2)):
                return self.nu[1]
            elif ((j in self.low1) and (i in self.low2)):
                return self.nu[1]-self.nu[0]
            else:
                print 'interaction_freq error\n'
                print i,j

    def rotating_wave_approx(self,freqs):
        #if 0 in self.efreq+self.interaction_freq(i,k):
        efrequency = self.efreq.copy()
        for f in freqs:
            efrequency += f
        if 0 in efrequency:
            return True
        else:
            print 'frequency droped!'
            print efrequency

    def diagonal_part(self,system,i,j):
        complex_tmp = np.zeros(self.N,dtype='complex')
        """
        plus part
        """
        for k in range(self.n):
            if k==j: # diagonal hamiltonian
                complex_tmp[self.density_index(i,k)]+=1j*self.hamiltonian(k,j)
            else:
                if k>i:
                    #if 0 in self.efreq+self.interaction_freq(i,k):
                    if self.rotating_wave_approx([self.interaction_freq(i,k)]):
                        complex_tmp[self.density_index(i,k)]+=1j*self.hamiltonian(k,j)/2
                        complex_tmp[self.density_index(i,k)+1]+= -1*self.hamiltonian(k,j)/2
                else:
                    if self.rotating_wave_approx([self.interaction_freq(i,k)]):
                    #if 0 in self.efreq+self.interaction_freq(i,k):
                        complex_tmp[self.density_index(k,i)]+=1j*self.hamiltonian(k,j)/2
                        complex_tmp[self.density_index(k,i)+1]+= self.hamiltonian(k,j)/2
        """
        minus part
        """
        for k in range(self.n):
            if k==i: # diagonal hamiltonian
                complex_tmp[self.density_index(k,j)]-=1j*self.hamiltonian(i,k)
            else:
                if j>k:
                    if self.rotating_wave_approx([self.interaction_freq(k,j)]):                                                 #if 0 in self.efreq+self.interaction_freq(k,j):
                        complex_tmp[self.density_index(k,j)]-=1j*self.hamiltonian(i,k)/2
                        complex_tmp[self.density_index(k,j)+1]-= -1*self.hamiltonian(i,k)/2
                else:
                    #if 0 in self.efreq+self.interaction_freq(k,j):
                    if self.rotating_wave_approx([self.interaction_freq(k,j)]):
                        complex_tmp[self.density_index(j,k)]-=1j*self.hamiltonian(i,k)/2
                        complex_tmp[self.density_index(j,k)+1]-= self.hamiltonian(i,k)/2
        for num in complex_tmp:
            if num.imag !=0:
                raise IOError('complex number in density matrix diagonal!')
        for s in range(self.N):
            system[self.density_index(i,j)][s] = complex_tmp[s].real
        return system

    def non_diagonal_part(self,system,i,j):
        complex_tmp = np.zeros(self.N,dtype='complex')
        """
        plus part
        """
        for k in range(self.n):
            if k==j: # diagonal hamiltonian
                if self.interaction_freq(i,k)-self.interaction_freq(i,j) == 0: #always same can be delete
                    complex_tmp[self.density_index(i,k)] += 1j*self.hamiltonian(k,j)
                    complex_tmp[self.density_index(i,k)+1] += -1*self.hamiltonian(k,j)
            else:
                if i==k: #rho_ii
                    #if 0 in self.efreq+self.interaction_freq(i,k)-self.interaction_freq(i,j):
                    if self.rotating_wave_approx([self.interaction_freq(i,k),-1*self.interaction_freq(i,j)]):                        
                        complex_tmp[self.density_index(i,k)]+=1j*self.hamiltonian(k,j)/2
                elif k>i: #rho_ik, upper diagonal
                    #if 0 in self.efreq+self.interaction_freq(i,k)-self.interaction_freq(i,j):
                    if self.rotating_wave_approx([self.interaction_freq(i,k),-1*self.interaction_freq(i,j)]):                                                
                        complex_tmp[self.density_index(i,k)]+=1j*self.hamiltonian(k,j)/2
                        complex_tmp[self.density_index(i,k)+1]+= -1*self.hamiltonian(k,j)/2
                else: # lower diagonal
                    #if 0 in self.efreq+self.interaction_freq(i,k)-self.interaction_freq(i,j):
                    if self.rotating_wave_approx([self.interaction_freq(i,k),-1*self.interaction_freq(i,j)]):                                            
                        complex_tmp[self.density_index(k,i)]+=1j*self.hamiltonian(k,j)/2
                        complex_tmp[self.density_index(k,i)+1]+= self.hamiltonian(k,j)/2
        """
        minus part
        """
        for k in range(self.n):
            if k==i: # diagonal hamiltonian
                if self.interaction_freq(k,j)-self.interaction_freq(i,j) == 0: #always same can be delete
                    complex_tmp[self.density_index(k,j)] -= 1j*self.hamiltonian(i,k)
                    complex_tmp[self.density_index(k,j)+1] -= -1*self.hamiltonian(i,k)
            else:
                if j==k:
                    #if 0 in self.efreq+self.interaction_freq(k,j)-self.interaction_freq(i,j):
                    if self.rotating_wave_approx([self.interaction_freq(k,j),-1*self.interaction_freq(i,j)]):                                                
                        complex_tmp[self.density_index(k,j)]-= 1j*self.hamiltonian(i,k)/2
                elif j>k:
                    #if 0 in self.efreq+self.interaction_freq(k,j)-self.interaction_freq(i,j):
                    if self.rotating_wave_approx([self.interaction_freq(k,j),-1*self.interaction_freq(i,j)]):                                                                    
                        complex_tmp[self.density_index(k,j)]-=1j*self.hamiltonian(i,k)/2
                        complex_tmp[self.density_index(k,j)+1]-= -1*self.hamiltonian(i,k)/2
                else:
                    #if 0 in self.efreq+self.interaction_freq(k,j)-self.interaction_freq(i,j):
                    if self.rotating_wave_approx([self.interaction_freq(k,j),-1*self.interaction_freq(i,j)]):                                                                    
                        complex_tmp[self.density_index(j,k)]-=1j*self.hamiltonian(i,k)/2
                        complex_tmp[self.density_index(j,k)+1]-= self.hamiltonian(i,k)/2
        for s in range(self.N):
            system[self.density_index(i,j)][s] = complex_tmp[s].real
            system[self.density_index(i,j)+1][s] = complex_tmp[s].imag
        return system

    def decoherence(self,system):
        system[self.density_index(0,0)][self.density_index(0,0)]-=self.Gamma1
        system[self.density_index(1,1)][self.density_index(0,0)]+=self.Gamma12
        system[self.density_index(1,1)][self.density_index(1,1)]-=self.gamma1
        system[self.density_index(1,1)][self.density_index(2,2)]+=self.gamma2
        system[self.density_index(0,1)][self.density_index(0,1)]-=0.5*self.Gamma1
        system[self.density_index(0,1)+1][self.density_index(0,1)+1]-=0.5*self.Gamma1
        system[self.density_index(0,2)][self.density_index(0,2)]-=0.5*self.Gamma1
        system[self.density_index(0,2)+1][self.density_index(0,2)+1]-=0.5*self.Gamma1
        system[self.density_index(1,2)][self.density_index(1,2)]-=self.gamma2
        system[self.density_index(1,2)+1][self.density_index(1,2)+1]-=self.gamma2
        return system

    def add_freq(self,system):
        for i in range(self.n):
            for j in range(self.n):
                if j>i:
                    system[self.density_index(i,j)][self.density_index(i,j)+1]+=self.interaction_freq(i,j)
                    system[self.density_index(i,j)+1][self.density_index(i,j)]-=self.interaction_freq(i,j)

        return system

    def sweep(self,start,end,points):
        counter = 0 # progress bar's counter
        f=open('./test.txt','w')
        prog = ProgressBar(counter, points, 50, mode='fixed', char='#')
        for freq in np.linspace(start,end,points):
            counter +=1
            prog.increment_amount()
            print prog, '\r',
            sys.stdout.flush()
            system_sweep = self.system.copy()
            # keep self.system independant of frequency,
            # only do frequency dependent operation on system_sweep
            self.nu[0]=self.nu2[0]+freq
            system_sweep = self.add_freq(system_sweep)
            system_sweep=np.matrix(system_sweep)
            solution = np.linalg.solve(system_sweep,self.a)
            f.write('%.0f %.8f %.8f %.8f\n'%(freq,solution[0,0],solution[5,0],solution[8,0]))


    def von_neumann(self,system):
        for i in range(self.n):
            for j in range(self.n):
                #for every density matrix element
                if j>i and ([i,j] != [self.n-1,self.n-1]):
                    self.non_diagonal_part(system,i,j)
                """
                diagonal element of density matrix
                """
                if j==i and ([i,j] != [self.n-1,self.n-1]):
                    self.diagonal_part(system,i,j)
                else:
                    pass
        return system

    def __init__(self,n,omega,dipole,nu,up,low1,low2,Gamma1,Gamma12,Gamma13,gamma1,gamma2 ):
        """
        """
        self.n = n
        self.omega = omega
        self.dipole = dipole
        self.nu = nu
        self.nu2 = self.nu[:]
        self.up = up
        self.low1 = low1
        self.low2 = low2
        self.Gamma1=Gamma1
        self.Gamma12=Gamma12
        self.Gamma13=Gamma13
        self.gamma1=gamma1
        self.gamma2=gamma2
        self.efreq = np.array([-1*nu[0],nu[0],-1*nu[1],nu[1]]) # frequencies of electric field
        self.groups = [up,low1,low2]
        self.N=self.density_length(n)
        self.a=np.zeros(self.N)
        self.a[self.N-1]=1
        self.a=np.matrix(self.a)
        self.a=self.a.T
        self.system=np.zeros([self.N,self.N])
        self.system=self.normalize(self.system)
        self.system=self.von_neumann(self.system)
        self.system=self.decoherence(self.system)

if __name__ ==  '__main__':
    an=3
    aomega = [351E12,9E9,0]
    adipole=[[0,1000000,1000000],
            [1000000,0,0],
            [1000000,0,0]]
    #remember to /2
    anu=[351E12-9E9,351E12] # on resonence
    aup = [0]
    alow1 = [1]
    alow2 = [2]
    #decoherence
    aGamma1 = 5000000
    aGamma12 = 2500000
    aGamma13 = 2500000
    agamma1 = 10000
    agamma2 = 10000

    system = System(an,aomega,adipole,anu,aup,alow1,alow2,aGamma1,aGamma12,aGamma13,agamma1,agamma2)
    system.sweep(-1E7,1E7,1000)
