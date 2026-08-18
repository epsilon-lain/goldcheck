#include <bits/stdc++.h>
#include <omp.h>
using namespace std;using i128=__int128_t;using i64=long long;
static inline i64 fd(i128 a,i128 b){i128 q=a/b,r=a%b;if(r&&a<0)--q;return(i64)q;}
struct Rat{long long n,d;};
const int Dv[4]={25,49,11,17};
const int denv[16]={1,25,49,1225,11,275,539,13475,17,425,833,20825,187,4675,9163,229075};
const int csv[16]={1,6,8,48,1,6,8,48,1,6,8,48,1,6,8,48};
const int lowv[16]={1,-5,9,-445,6,-80,14,-5880,12,-110,68,-8550,67,-1605,-157,-108885};
const int highv[16]={1,19,41,731,10,184,402,6864,16,298,648,11250,159,2859,6303,104283};
const Rat lam[16]={{0,1},{3,4},{247,1000},{169,200},{177,1000},{409,500},{347,500},{937,1000},{33,500},{831,1000},{173,250},{461,500},{87,125},{903,1000},{213,250},{541,500}};
const Rat nu[16]={{197,500},{113,1000},{428,125},{951,1000},{2233,500},{947,500},{10,1},{10,1},{6731,1000},{221,1000},{10,1},{10,1},{10,1},{10,1},{10,1},{10,1}};
const long long Q=1000000000LL,CD=100000LL;
const int linM[10]={3,5,6,7,9,10,11,12,13,14};const long long linC[10]={75226,37691,35316,79381,25053,31897,66042,8400,68044,55875};
const int crS[21]={1,1,1,2,3,3,3,3,3,3,4,5,5,6,7,7,9,9,10,11,12};const int crT[21]={3,5,9,6,5,7,9,10,11,14,12,7,9,10,9,12,10,11,13,13,14};const long long crC[21]={0,31340,33295,13131,3625,26690,9985,0,74074,0,78405,47933,119720,213049,12600,0,0,88753,0,637381,0};
const long long facC[12]={5148,3263,882,820,2663,1601,434,211,894,668,625,280};const int um[11]={3,5,6,7,9,10,11,12,13,14,15};
vector<i64> phiTab[16];
static inline i64 phi_floor(int C,int n){int T=15^C;Rat L=lam[T],N=nu[T];i128 a=(i128)L.n*denv[C]-(i128)n*L.d,b=(i128)L.d*denv[C],xn=-a*N.d,xd=(i128)2*N.n*b; i128 lon=(i128)14*csv[T],lod=(i128)169*denv[T],hin=5*lon,hid=lod,xnum,xden;if(xn*lod<lon*xd){xnum=lon;xden=lod;}else if(xn*hid>hin*xd){xnum=hin;xden=hid;}else return fd(-(i128)a*a*N.d*Q,(i128)4*N.n*b*b);i128 num=(i128)N.n*xnum*xnum*b+a*xnum*N.d*xden,den=(i128)N.d*xden*xden*b;return fd(num*Q,den);}
static inline void rho_nums(int A1,int B1,int A2,int B2,int z3,int z4,int bits,long long n[16],long long t[16]){memset(t,0,16*sizeof(long long));t[1]=6+5*A1+B1;t[2]=8+7*A2+B2;t[4]=z3;t[8]=z4;for(int j=0;j<11;j++){int m=um[j],z=(bits>>j&1)?5:1;t[m]=(long long)csv[m]*z;}memset(n,0,16*sizeof(long long));n[0]=1;for(int sz=1;sz<=4;sz++)for(int C=1;C<16;C++)if(__builtin_popcount((unsigned)C)==sz){int p=C&-C,i=__builtin_ctz((unsigned)p),rest=C^p;long long v=(long long)Dv[i]*n[rest];int T=rest;while(1){int S=p|T;v-=t[S]*n[C^S];if(!T)break;T=(T-1)&rest;}n[C]=v;}}
static i64 pcfun(){i64 o=0;for(int T=0;T<16;T++){i128 lon=(i128)14*csv[T],lod=(i128)169*denv[T];o+=fd((i128)lam[T].n*lon*Q,(i128)lam[T].d*lod);o+=fd((i128)nu[T].n*lon*lon*Q,(i128)nu[T].d*lod*lod);}return o;}
static inline i64 eval(int A1,int B1,int A2,int B2,int z3,int z4,int bits,i64 pcf){long long n[16],t[16];rho_nums(A1,B1,A2,B2,z3,z4,bits,n,t);i64 full=fd((i128)n[15]*Q,denv[15]);for(int C=0;C<16;C++)full+=phiTab[C][n[C]-lowv[C]];i64 mr=LLONG_MAX;for(int C=1;C<16;C++)mr=min(mr,fd((i128)n[C]*Q,denv[C]));i64 val=min(full,mr+pcf);for(int k=0;k<10;k++){int m=linM[k];val+=fd((i128)linC[k]*t[m]*Q,(i128)CD*denv[m]);}for(int k=0;k<21;k++)if(crC[k]){int s=crS[k],u=crT[k];val+=fd((i128)crC[k]*t[s]*t[u]*Q,(i128)CD*denv[s]*denv[u]);}int acts[6]={A1,B1,A2,B2,z3-1,z4-1};for(int j=0;j<6;j++){long long a=acts[j];val+=(i64)((i128)facC[2*j]*a*(Q/CD));val+=(i64)((i128)facC[2*j+1]*(a*(a-1)/2)*(Q/CD));}return val;}
int main(){for(int C=0;C<16;C++){phiTab[C].resize(highv[C]-lowv[C]+1);for(int n=lowv[C];n<=highv[C];n++)phiTab[C][n-lowv[C]]=phi_floor(C,n);}i64 pcf=pcfun(),best=LLONG_MAX;long long bc=-1,total=25LL*25*5*5*(1<<11);
#pragma omp parallel
{i64 lb=LLONG_MAX;long long lc=-1;
#pragma omp for schedule(static)
for(long long code=0;code<total;code++){long long z=code;int bits=z&2047;z>>=11;int z4=z%5+1;z/=5;int z3=z%5+1;z/=5;int B2=z%5;z/=5;int A2=z%5;z/=5;int B1=z%5;z/=5;int A1=z%5;i64 v=eval(A1,B1,A2,B2,z3,z4,bits,pcf);if(v<lb){lb=v;lc=code;}}
#pragma omp critical
if(lb<best){best=lb;bc=lc;}
}
long long z=bc;int bits=z&2047;z>>=11;int z4=z%5+1;z/=5;int z3=z%5+1;z/=5;int B2=z%5;z/=5;int A2=z%5;z/=5;int B1=z%5;z/=5;int A1=z%5;cout<<best<<" "<<A1<<" "<<B1<<" "<<A2<<" "<<B2<<" "<<z3<<" "<<z4<<" "<<bits<<" pcf="<<pcf<<"\n";}
