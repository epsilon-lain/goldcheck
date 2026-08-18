#include <bits/stdc++.h>
#include <omp.h>
using namespace std;
using i128 = __int128_t;
using i64 = long long;

static inline i64 floordiv128(i128 a, i128 b){
    i128 q=a/b, r=a%b;
    if(r!=0 && a<0) --q;
    return (i64)q;
}
struct Rat { long long n,d; };

const int Dv[4]={49,121,13,17};
const int denv[16]={1,49,121,5929,13,637,1573,77077,17,833,2057,100793,221,10829,26741,1310309};
const int csv[16]={1,8,12,96,1,8,12,96,1,8,12,96,1,8,12,96};
const int lowv[16]={1,9,61,69,8,32,428,-2908,12,68,672,-2632,91,-21,4291,-82637};
const int highv[16]={1,41,109,4373,12,484,1296,51016,16,648,1732,68508,191,7599,20471,793095};

// Coefficients for special masks 1|(T<<1), T=0,...,15.
const Rat lam[16]={
{0,1},{3,4},{247,1000},{169,200},{177,1000},{409,500},{347,500},{937,1000},
{33,500},{831,1000},{173,250},{461,500},{87,125},{903,1000},{213,250},{541,500}};
const Rat nu[16]={
{197,500},{113,1000},{428,125},{951,1000},{2233,500},{947,500},{10,1},{10,1},
{6731,1000},{221,1000},{10,1},{10,1},{10,1},{10,1},{10,1},{10,1}};

const long long Q=1000000000LL;
const long long CDEN=100000LL;
const int linM[10]={3,5,6,7,9,10,11,12,13,14};
const long long linC[10]={29487,24837,29050,53691,19677,28831,49236,18917,51820,40706};
const int crS[21]={1,1,1,2,3,3,3,3,3,3,4,5,5,6,7,7,9,9,10,11,12};
const int crT[21]={3,5,9,6,5,7,9,10,11,14,12,7,9,10,9,12,10,11,13,13,14};
const long long crC[21]={37491,39778,42878,9140,39045,133887,42725,0,145320,53495,33261,88993,37559,57052,0,0,0,81843,0,914418,61883};
const long long facC[12]={2433,1413,425,184,995,844,118,55,826,504,610,312};
const int um[11]={3,5,6,7,9,10,11,12,13,14,15};
vector<i64> phiTab[16];

static inline i64 phi_floor(int C,int n){
    int T=15^C;
    Rat L=lam[T], N=nu[T];
    i128 a=(i128)L.n*denv[C]-(i128)n*L.d;
    i128 b=(i128)L.d*denv[C];
    i128 xn=-a*N.d, xd=(i128)2*N.n*b;
    i128 lon=(i128)6*csv[T], lod=(i128)25*denv[T];
    i128 hin=5*lon, hid=lod;
    i128 xnum,xden;
    if(xn*lod < lon*xd){ xnum=lon; xden=lod; }
    else if(xn*hid > hin*xd){ xnum=hin; xden=hid; }
    else {
        i128 num=-(i128)a*a*N.d*Q;
        i128 den=(i128)4*N.n*b*b;
        return floordiv128(num,den);
    }
    i128 num=(i128)N.n*xnum*xnum*b + a*xnum*N.d*xden;
    i128 den=(i128)N.d*xden*xden*b;
    return floordiv128(num*Q,den);
}

static inline void rho_nums(
    int A7,int B7,int A11,int B11,int z13,int z17,int bits,
    long long n[16], long long t[16]){
    memset(t,0,16*sizeof(long long));
    t[1]=8+7*A7+B7;
    t[2]=12+11*A11+B11;
    t[4]=z13;
    t[8]=z17;
    for(int j=0;j<11;j++){
        int m=um[j];
        int z=(bits>>j&1)?5:1;
        t[m]=(long long)csv[m]*z;
    }

    memset(n,0,16*sizeof(long long));
    n[0]=1;
    for(int sz=1;sz<=4;sz++){
        for(int C=1;C<16;C++){
            if(__builtin_popcount((unsigned)C)!=sz) continue;
            int pivot=C&-C;
            int i=__builtin_ctz((unsigned)pivot);
            int rest=C^pivot;
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

static i64 pcoord_floor(){
    i64 out=0;
    for(int T=0;T<16;T++){
        i128 lon=(i128)6*csv[T], lod=(i128)25*denv[T];
        out += floordiv128((i128)lam[T].n*lon*Q,(i128)lam[T].d*lod);
        out += floordiv128((i128)nu[T].n*lon*lon*Q,(i128)nu[T].d*lod*lod);
    }
    return out;
}

static inline i64 eval_state(
    int A7,int B7,int A11,int B11,int z13,int z17,int bits,i64 pcf){
    long long n[16],t[16];
    rho_nums(A7,B7,A11,B11,z13,z17,bits,n,t);

    i64 full=floordiv128((i128)n[15]*Q,denv[15]);
    for(int C=0;C<16;C++)
        full += phiTab[C][n[C]-lowv[C]];

    i64 minrho=LLONG_MAX;
    for(int C=1;C<16;C++)
        minrho=min(minrho,floordiv128((i128)n[C]*Q,denv[C]));
    i64 val=min(full,minrho+pcf);

    for(int k=0;k<10;k++){
        int m=linM[k];
        val += floordiv128((i128)linC[k]*t[m]*Q,(i128)CDEN*denv[m]);
    }
    for(int k=0;k<21;k++){
        int s=crS[k],u=crT[k];
        if(crC[k])
            val += floordiv128((i128)crC[k]*t[s]*t[u]*Q,
                               (i128)CDEN*denv[s]*denv[u]);
    }

    int acts[6]={A7,B7,A11,B11,z13-1,z17-1};
    for(int j=0;j<6;j++){
        long long a=acts[j];
        val += (i64)((i128)facC[2*j]*a*(Q/CDEN));
        val += (i64)((i128)facC[2*j+1]*(a*(a-1)/2)*(Q/CDEN));
    }
    return val;
}

int main(){
    for(int C=0;C<16;C++){
        phiTab[C].resize(highv[C]-lowv[C]+1);
        for(int n=lowv[C];n<=highv[C];n++)
            phiTab[C][n-lowv[C]]=phi_floor(C,n);
    }
    i64 pcf=pcoord_floor();
    long long total=25LL*25*5*5*(1<<11);
    i64 globalBest=LLONG_MAX;
    long long bestCode=-1;

    #pragma omp parallel
    {
        i64 localBest=LLONG_MAX;
        long long localCode=-1;
        #pragma omp for schedule(static)
        for(long long code=0;code<total;code++){
            long long z=code;
            int bits=z&2047; z>>=11;
            int z17=z%5+1; z/=5;
            int z13=z%5+1; z/=5;
            int B11=z%5; z/=5;
            int A11=z%5; z/=5;
            int B7=z%5; z/=5;
            int A7=z%5;
            i64 v=eval_state(A7,B7,A11,B11,z13,z17,bits,pcf);
            if(v<localBest){ localBest=v; localCode=code; }
        }
        #pragma omp critical
        if(localBest<globalBest){ globalBest=localBest; bestCode=localCode; }
    }

    long long z=bestCode;
    int bits=z&2047; z>>=11;
    int z17=z%5+1; z/=5;
    int z13=z%5+1; z/=5;
    int B11=z%5; z/=5;
    int A11=z%5; z/=5;
    int B7=z%5; z/=5;
    int A7=z%5;
    cout << globalBest << " " << A7 << " " << B7 << " "
         << A11 << " " << B11 << " " << z13 << " " << z17 << " "
         << bits << "\n";
    return 0;
}
