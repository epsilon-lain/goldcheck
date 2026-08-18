// M64 exact fast verifier for 3^3*5^2*7^2*11^2*13^2*17^2.
// Expected output:
// 3359197 2 1 1 3 1 2 1 0 335
// Q=10^7, so 3359197 > 3359000 = Q*(3359/10000).
#include <bits/stdc++.h>
#include <omp.h>
using namespace std; using i128=__int128_t; using i64=long long;
static inline i64 fd(i128 a,i128 b){i128 q=a/b,r=a%b;if(r&&a<0)--q;return (i64)q;}
struct Rat{long long n,d;};
const int Dv[4]={49,121,169,289};
const long long denv[16]={1,49,121,5929,169,8281,20449,1002001,289,14161,34969,1713481,48841,2393209,5909761,289578289};
const long long csv[16]={1,8,12,96,14,112,168,1344,18,144,216,1728,252,2016,3024,24192};
const long long lowv[16]={1,17,73,857,113,1473,7577,47337,217,3113,14977,122321,23513,229353,1460897,2099121};
const long long highv[16]={1,41,109,4373,155,6243,16727,657375,271,10967,29323,1158803,41753,1657185,4469045,172653693};
const Rat lam[16]={{0,1},{3,4},{247,1000},{169,200},{177,1000},{409,500},{347,500},{937,1000},{33,500},{831,1000},{173,250},{461,500},{87,125},{903,1000},{213,250},{541,500}};
const Rat nu[16]={{197,500},{113,1000},{428,125},{951,1000},{2233,500},{947,500},{10,1},{10,1},{6731,1000},{221,1000},{10,1},{10,1},{10,1},{10,1},{10,1},{10,1}};
const i64 Q=10000000LL;
const int linM[9]={3,5,6,7,9,11,13,14,15}; const int linC[9]={260,342,172,600,124,326,219,118,645};
const int crS[19]={1,1,1,2,3,3,3,5,5,5,6,6,6,9,9,10,10,10,12};
const int crT[19]={3,9,11,10,10,11,15,9,12,13,10,12,14,10,13,11,12,14,13};
const int crC[19]={446,507,111,83,1120,2934,1781,1083,1630,4085,4355,5337,8418,1421,5446,5498,7240,9038,2465};
const int facC[16]={25,2,14,6,8,1,11,0,11,0,4,1,6,1,4,1};
vector<i64> phiTab[16];
static inline i64 phi_floor(int C,long long n){int T=15^C; Rat L=lam[T],N=nu[T]; i128 a=(i128)L.n*denv[C]-(i128)n*L.d; i128 b=(i128)L.d*denv[C]; i128 xn=-a*N.d, xd=(i128)2*N.n*b; i128 lon=(i128)6*csv[T],lod=(i128)25*denv[T],hin=4*lon,hid=lod; i128 xnum,xden; if(xn*lod<lon*xd){xnum=lon;xden=lod;} else if(xn*hid>hin*xd){xnum=hin;xden=hid;} else {i128 num=-(i128)a*a*N.d*Q,den=(i128)4*N.n*b*b;return fd(num,den);} i128 num=(i128)N.n*xnum*xnum*b+a*xnum*N.d*xden; i128 den=(i128)N.d*xden*xden*b;return fd(num*Q,den);}
static inline void rho_nums(int A7,int B7,int A11,int B11,int A13,int B13,int A17,int B17,int ebits,long long n[16],long long t[16]){memset(t,0,16*sizeof(long long));t[1]=8+7*A7+B7;t[2]=12+11*A11+B11;t[4]=14+13*A13+B13;t[8]=18+17*A17+B17;const int um[11]={3,5,6,7,9,10,11,12,13,14,15};for(int j=0;j<11;j++){int m=um[j];int z=(ebits>>j&1)?4:1;t[m]=csv[m]*z;}memset(n,0,16*sizeof(long long));n[0]=1;for(int sz=1;sz<=4;sz++)for(int C=1;C<16;C++){if(__builtin_popcount((unsigned)C)!=sz)continue;int pivot=C&-C,i=__builtin_ctz((unsigned)pivot),rest=C^pivot;long long v=(long long)Dv[i]*n[rest];int T=rest;while(true){int S=pivot|T;v-=t[S]*n[C^S];if(!T)break;T=(T-1)&rest;}n[C]=v;}}
static inline i64 eval_state(int A7,int B7,int A11,int B11,int A13,int B13,int A17,int B17,int ebits){
    long long n[16],t[16]; rho_nums(A7,B7,A11,B11,A13,B13,A17,B17,ebits,n,t);
    i64 val=fd((i128)n[15]*Q,denv[15]);
    for(int C=0;C<15;C++) val+=phiTab[C][n[C]-lowv[C]]; val+=phi_floor(15,n[15]);
    for(int k=0;k<9;k++){int m=linM[k];val+=fd((i128)linC[k]*t[m]*Q,(i128)1000*denv[m]);}
    for(int k=0;k<19;k++){int ss=crS[k],u=crT[k];val+=fd((i128)crC[k]*t[ss]*t[u]*Q,(i128)1000*denv[ss]*denv[u]);}
    long long units=0;int As[6]={A7,B7,A11,B11,A13,B13};int kk=0;
    for(int j=0;j<6;j+=2){int A=As[j],B=As[j+1];units+=(long long)facC[kk]*A+(long long)facC[kk+1]*B+(long long)facC[kk+2]*(A*(A-1)/2)+(long long)facC[kk+3]*(B*(B-1)/2);kk+=4;}
    units += (long long)facC[12]*A17 + (long long)facC[13]*B17 + (long long)facC[14]*(A17*(A17-1)/2) + (long long)facC[15]*(B17*(B17-1)/2);
    val+=units*(Q/1000); return val;
}
int main(){
    for(int C=0;C<15;C++){phiTab[C].resize(highv[C]-lowv[C]+1);for(long long n=lowv[C];n<=highv[C];n++) phiTab[C][n-lowv[C]]=phi_floor(C,n);}
    i64 gb=LLONG_MAX; unsigned long long bc=0;
    #pragma omp parallel
    {
        i64 lb=LLONG_MAX; unsigned long long lc=0;
        #pragma omp for schedule(static)
        for(int ii=0;ii<65536;ii++){
            int A7=(ii/16384)%4,B7=(ii/4096)%4,A11=(ii/1024)%4,B11=(ii/256)%4,A13=(ii/64)%4,B13=(ii/16)%4,A17=(ii/4)%4,B17=ii%4;
            for(int ep=0;ep<2048;ep++){
                i64 v=eval_state(A7,B7,A11,B11,A13,B13,A17,B17,ep);
                if(v<lb){lb=v;lc=(unsigned long long)ii*2048+ep;}
            }
        }
        #pragma omp critical
        { if(lb<gb){gb=lb;bc=lc;} }
    }
    unsigned long long ii=bc/2048; int ep=bc%2048;
    int A7=(ii/16384)%4,B7=(ii/4096)%4,A11=(ii/1024)%4,B11=(ii/256)%4,A13=(ii/64)%4,B13=(ii/16)%4,A17=(ii/4)%4,B17=ii%4;
    cout<<gb<<" "<<A7<<" "<<B7<<" "<<A11<<" "<<B11<<" "<<A13<<" "<<B13<<" "<<A17<<" "<<B17<<" "<<ep<<"\n";
}
