// M68 exact exhaustive verifier for
//   3^4 * 5^2 * 7^2 * 11^2 * 13 * 17.
//
// It checks the 25^2 * 5^2 * 2^11 = 32,000,000 reduced states of the
// double-weighted-square goodness certificate. Every rational contribution is
// rounded downward at scale Q=1e9, so the reported global minimum is a rigorous
// lower bound for the exact pointwise certificate.
//
// Expected output:
//   347959679 0 0 0 0 1 1 0
// and 347959679 > Q*(34795/100000) = 347950000.
//
#include <bits/stdc++.h>
#include <omp.h>
using namespace std;
using i128=__int128_t;
using i64=long long;
struct Rat{ long long n,d; };
static inline i64 floordiv128(i128 a,i128 b){
    i128 q=a/b, r=a%b;
    if(r!=0 && a<0) --q;
    return (i64)q;
}
const long long Q=1000000000LL;
const long long CD=1000000LL;
const int Dv[4]={49,121,13,17};
const int denv[16]={1,49,121,5929,13,637,1573,77077,17,833,2057,100793,221,10829,26741,1310309};
const int csv[16]={1,8,12,96,1,8,12,96,1,8,12,96,1,8,12,96};
const int lowv[16]={1,9,61,69,8,32,428,-2908,12,68,672,-2632,91,-21,4291,-82637};
const int highv[16]={1,41,109,4373,12,484,1296,51016,16,648,1732,68508,191,7599,20471,793095};
const Rat lam[16]={{0,1},{3,4},{247,1000},{169,200},{177,1000},{409,500},{347,500},{937,1000},{33,500},{831,1000},{173,250},{461,500},{87,125},{903,1000},{213,250},{541,500}};
const Rat nu[16]={{197,500},{113,1000},{428,125},{951,1000},{2233,500},{947,500},{10,1},{10,1},{6731,1000},{221,1000},{10,1},{10,1},{10,1},{10,1},{10,1},{10,1}};
const long long PCOORD_FLOOR=78658753LL;
const int NL=11;
const int linM[NL]={3,5,6,7,9,10,11,12,13,14,15};
const long long linC[NL]={299988,241193,276475,506889,201268,206611,446165,133302,361344,380235,661097};
const int NP=32;
const int pairS[NP]={1,1,1,1,1,1,2,2,2,3,3,3,3,3,4,5,5,5,5,6,6,6,7,7,7,8,9,9,10,10,11,11};
const int pairT[NP]={3,5,7,9,11,13,6,10,14,5,7,9,11,15,12,7,9,13,15,10,12,14,11,13,15,12,11,13,12,14,13,15};
const long long pairC[NP]={382568,411361,14485,428912,62436,204817,134032,271704,62928,365281,1035159,325072,1302286,660125,333243,1025825,282823,1304830,256337,421152,136703,812335,6428064,2762026,3929384,295228,1001449,1327325,348076,518787,2189698,5138425};
const long long facC[12]={23938,14204,4242,1863,9824,8107,1160,584,8180,5282,6182,3034};

const int um[11]={3,5,6,7,9,10,11,12,13,14,15};
vector<i64> phiTab[16];

static inline i64 phi_floor(int C,int n){
    int T=15^C;
    Rat La=lam[T], Nu=nu[T];
    i128 a=(i128)La.n*denv[C]-(i128)n*La.d;
    i128 b=(i128)La.d*denv[C];
    i128 xn=-a*Nu.d;
    i128 xd=(i128)2*Nu.n*b;
    i128 lon=(i128)6*csv[T], lod=(i128)25*denv[T];
    i128 hin=5*lon, hid=lod;
    i128 xnum,xden;
    if(xn*lod < lon*xd){ xnum=lon; xden=lod; }
    else if(xn*hid > hin*xd){ xnum=hin; xden=hid; }
    else{
        i128 num=-(i128)a*a*Nu.d*Q;
        i128 dd=(i128)4*Nu.n*b*b;
        return floordiv128(num,dd);
    }
    i128 num=(i128)Nu.n*xnum*xnum*b + a*xnum*Nu.d*xden;
    i128 dd=(i128)Nu.d*xden*xden*b;
    return floordiv128(num*Q,dd);
}
static inline void rho_nums(int A7,int B7,int A11,int B11,int z13,int z17,int bits,
                            long long n[16],long long t[16]){
    memset(t,0,16*sizeof(long long));
    t[1]=8+7*A7+B7;
    t[2]=12+11*A11+B11;
    t[4]=z13;
    t[8]=z17;
    for(int j=0;j<11;j++){
        int m=um[j];
        t[m]=(long long)csv[m]*(((bits>>j)&1)?5:1);
    }
    memset(n,0,16*sizeof(long long)); n[0]=1;
    for(int sz=1;sz<=4;sz++){
        for(int C=1;C<16;C++){
            if(__builtin_popcount((unsigned)C)!=sz) continue;
            int pivot=C&-C, i=__builtin_ctz((unsigned)pivot), rest=C^pivot;
            long long v=(long long)Dv[i]*n[rest];
            int T=rest;
            while(true){
                int S=pivot|T;
                v-=t[S]*n[C^S];
                if(T==0) break;
                T=(T-1)&rest;
            }
            n[C]=v;
        }
    }
}
static inline i64 eval_state(int A7,int B7,int A11,int B11,int z13,int z17,int bits){
    long long n[16],t[16]; rho_nums(A7,B7,A11,B11,z13,z17,bits,n,t);
    i64 full=floordiv128((i128)n[15]*Q,denv[15]);
    for(int C=0;C<16;C++){
        int idx=n[C]-lowv[C];
        if(idx<0 || n[C]>highv[C]){ cerr<<"range error\n"; abort(); }
        full += phiTab[C][idx];
    }
    i64 mr=LLONG_MAX;
    for(int C=1;C<16;C++){
        i64 rr=floordiv128((i128)n[C]*Q,denv[C]);
        if(rr<mr) mr=rr;
    }
    i64 coord=mr+PCOORD_FLOOR;
    i64 val=min(full,coord);
    for(int k=0;k<NL;k++){
        int m=linM[k];
        val += floordiv128((i128)linC[k]*t[m]*Q,(i128)CD*denv[m]);
    }
    for(int k=0;k<NP;k++){
        int s=pairS[k],u=pairT[k];
        val += floordiv128((i128)pairC[k]*t[s]*t[u]*Q,
                           (i128)CD*denv[s]*denv[u]);
    }
    int acts[6]={A7,B7,A11,B11,z13-1,z17-1};
    for(int j=0;j<6;j++){
        long long A=acts[j];
        val += facC[2*j]*A*(Q/CD);
        val += facC[2*j+1]*(A*(A-1)/2)*(Q/CD);
    }
    return val;
}
int main(){
    for(int C=0;C<16;C++){
        phiTab[C].resize((size_t)highv[C]-lowv[C]+1);
        for(int n=lowv[C];n<=highv[C];n++)
            phiTab[C][n-lowv[C]]=phi_floor(C,n);
    }
    i64 gb=LLONG_MAX; long long code=-1;
    #pragma omp parallel
    {
      i64 lb=LLONG_MAX; long long lc=-1;
      #pragma omp for schedule(static)
      for(long long aa=0;aa<15625LL;aa++){
        int z=aa;
        int z17=z%5+1; z/=5;
        int z13=z%5+1; z/=5;
        int B11=z%5; z/=5;
        int A11=z%5; z/=5;
        int B7=z%5; z/=5;
        int A7=z%5;
        for(int bits=0;bits<2048;bits++){
            i64 v=eval_state(A7,B7,A11,B11,z13,z17,bits);
            if(v<lb){lb=v;lc=aa*2048+bits;}
        }
      }
      #pragma omp critical
      if(lb<gb){gb=lb;code=lc;}
    }
    long long aa=code/2048; int bits=code%2048; int z=aa;
    int z17=z%5+1;z/=5; int z13=z%5+1;z/=5;
    int B11=z%5;z/=5; int A11=z%5;z/=5; int B7=z%5;z/=5; int A7=z%5;
    cout<<gb<<" "<<A7<<" "<<B7<<" "<<A11<<" "<<B11<<" "<<z13<<" "<<z17<<" "<<bits<<"\n";
}
