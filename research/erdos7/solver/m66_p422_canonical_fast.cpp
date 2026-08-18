// M66 exact exhaustive verifier for the canonical P422 hard family reference.
// Target reference: 3^4 * 5^2 * 7^2 * 11 * 13 * 17.
// Compile: g++ -O3 -fopenmp m66_p422_canonical_fast.cpp -o m66_p422_canonical_fast
// Expected output: 3396094 3 3 1 1 1 1299
// The first integer is a rigorous downward-rounded lower minimum at Q=10^7.
// Compare against Q*C = 3394000 for C=1697/5000.

#include <bits/stdc++.h>
#include <omp.h>
using namespace std;
using i128=__int128_t;
using i64=long long;
struct Rat{long long n,d;};
static inline i64 floordiv(i128 a,i128 b){
    i128 q=a/b,r=a%b; if(r!=0 && a<0)--q; return (i64)q;
}
const long long Q=10000000LL;
const int Dv[4]={49,11,13,17};
const int denv[16]={1,49,11,539,13,637,143,7007,17,833,187,9163,221,10829,2431,119119};
const int csv[16]={1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8};
const int lowv[16]={1,9,6,14,8,32,43,-213,12,68,67,-157,91,-21,441,-6407};
const int highv[16]={1,41,10,402,12,484,119,4695,16,648,159,6303,191,7599,1881,73057};
const Rat lam[16]={{0LL,1LL},{3LL,4LL},{247LL,1000LL},{169LL,200LL},{177LL,1000LL},{409LL,500LL},{347LL,500LL},{937LL,1000LL},{33LL,500LL},{831LL,1000LL},{173LL,250LL},{461LL,500LL},{87LL,125LL},{903LL,1000LL},{213LL,250LL},{541LL,500LL}};
const Rat nu[16]={{197LL,500LL},{113LL,1000LL},{428LL,125LL},{951LL,1000LL},{2233LL,500LL},{947LL,500LL},{10LL,1LL},{10LL,1LL},{6731LL,1000LL},{221LL,1000LL},{10LL,1LL},{10LL,1LL},{10LL,1LL},{10LL,1LL},{10LL,1LL},{10LL,1LL}};
const int LIN[15]={0,0,306,0,256,216,339,0,215,228,358,211,350,199,0};
const int CRS[105]={1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,5,5,5,5,5,5,5,5,5,5,6,6,6,6,6,6,6,6,6,7,7,7,7,7,7,7,7,8,8,8,8,8,8,8,9,9,9,9,9,9,10,10,10,10,10,11,11,11,11,12,12,12,13,13,14};
const int CRT[105]={2,3,4,5,6,7,8,9,10,11,12,13,14,15,3,4,5,6,7,8,9,10,11,12,13,14,15,4,5,6,7,8,9,10,11,12,13,14,15,5,6,7,8,9,10,11,12,13,14,15,6,7,8,9,10,11,12,13,14,15,7,8,9,10,11,12,13,14,15,8,9,10,11,12,13,14,15,9,10,11,12,13,14,15,10,11,12,13,14,15,11,12,13,14,15,12,13,14,15,13,14,15,14,15,15};
const int CR[105]={0,338,0,389,0,0,0,384,0,0,0,0,0,0,0,0,0,260,0,0,0,0,0,0,0,0,0,0,60,0,3079,0,184,312,1655,0,0,1277,0,0,0,0,0,0,0,0,12,0,0,0,0,2719,0,450,0,0,0,0,0,0,0,0,0,672,0,0,0,0,0,0,1040,0,0,10660,0,0,0,0,0,0,0,0,0,0,331,2885,0,0,0,0,0,0,11844,0,0,0,55709,0,0,0,7353,0,0,0,0};
const int FAC[10]={22,16,2,3,11,6,9,4,6,3};
const int ums[11]={3,5,6,7,9,10,11,12,13,14,15};
const i64 PCOORD=773375LL;
vector<i64> phiTab[16];

static inline i64 phi_floor(int C,int n){
    int T=15^C;
    Rat L=lam[T], N=nu[T];
    i128 a=(i128)L.n*denv[C]-(i128)n*L.d;
    i128 bb=(i128)L.d*denv[C];
    i128 xn=-a*N.d;
    i128 xd=(i128)2*N.n*bb;
    i128 lon=(i128)6*csv[T], lod=(i128)25*denv[T];
    i128 hin=5*lon, hid=lod;
    if(xn*lod < lon*xd){
        i128 xnum=lon,xden=lod;
        i128 num=(i128)N.n*xnum*xnum*bb + a*xnum*N.d*xden;
        i128 den=(i128)N.d*xden*xden*bb;
        return floordiv(num*Q,den);
    }
    if(xn*hid > hin*xd){
        i128 xnum=hin,xden=hid;
        i128 num=(i128)N.n*xnum*xnum*bb + a*xnum*N.d*xden;
        i128 den=(i128)N.d*xden*xden*bb;
        return floordiv(num*Q,den);
    }
    i128 num=-(i128)a*a*N.d*Q;
    i128 den=(i128)4*N.n*bb*bb;
    return floordiv(num,den);
}
static inline i64 rat_floor(long long n,long long d){
    return floordiv((i128)n*Q,d);
}
static inline void rho_nums(int A7,int B7,int z11,int z13,int z17,int eb,long long n[16],long long t[16]){
    memset(t,0,16*sizeof(long long));
    t[1]=8+7*A7+B7; t[2]=z11; t[4]=z13; t[8]=z17;
    for(int j=0;j<11;j++){int m=ums[j];int z=((eb>>j)&1)?5:1;t[m]=(long long)csv[m]*z;}
    memset(n,0,16*sizeof(long long));n[0]=1;
    for(int sz=1;sz<=4;sz++)for(int C=1;C<16;C++)if(__builtin_popcount((unsigned)C)==sz){
        int pivot=C&-C;int i=__builtin_ctz((unsigned)pivot);int rest=C^pivot;
        long long v=(long long)Dv[i]*n[rest];int T=rest;
        while(true){int S=pivot|T;v-=t[S]*n[C^S];if(T==0)break;T=(T-1)&rest;}
        n[C]=v;
    }
}
static inline i64 eval_state(int A7,int B7,int z11,int z13,int z17,int eb){
    long long n[16],t[16];rho_nums(A7,B7,z11,z13,z17,eb,n,t);
    i64 full=rat_floor(n[15],denv[15]);
    for(int C=0;C<16;C++) full += phiTab[C][n[C]-lowv[C]];
    i64 mc=LLONG_MAX;
    for(int C=1;C<16;C++) mc=min(mc,rat_floor(n[C],denv[C]));
    i64 base=min(full, mc+PCOORD);
    i64 feat=0;
    for(int m=1;m<16;m++){
        int c=LIN[m-1]; if(c) feat += floordiv((i128)c*t[m]*Q,(i128)1000*denv[m]);
    }
    for(int k=0;k<105;k++){
        int c=CR[k]; if(c) feat += floordiv((i128)c*t[CRS[k]]*t[CRT[k]]*Q,(i128)1000*denv[CRS[k]]*denv[CRT[k]]);
    }
    int acts[5]={A7,B7,z11-1,z13-1,z17-1};
    i64 units=0;
    for(int j=0;j<5;j++){
        int A=acts[j];
        units += (long long)FAC[2*j]*A + (long long)FAC[2*j+1]*(A*(A-1)/2);
    }
    feat += units*(Q/1000);
    return base+feat;
}
int main(){
    for(int C=0;C<16;C++){
        phiTab[C].resize(highv[C]-lowv[C]+1);
        for(int n=lowv[C];n<=highv[C];n++)phiTab[C][n-lowv[C]]=phi_floor(C,n);
    }
    i64 best=LLONG_MAX; long long code=-1;
    #pragma omp parallel
    {
      i64 lb=LLONG_MAX; long long lc=-1;
      #pragma omp for schedule(static)
      for(int head=0;head<3125;head++){
        int x=head;int z17=x%5+1;x/=5;int z13=x%5+1;x/=5;int z11=x%5+1;x/=5;int B7=x%5;x/=5;int A7=x%5;
        for(int eb=0;eb<2048;eb++){
            i64 v=eval_state(A7,B7,z11,z13,z17,eb);
            if(v<lb){lb=v;lc=(long long)head*2048+eb;}
        }
      }
      #pragma omp critical
      if(lb<best){best=lb;code=lc;}
    }
    long long head=code/2048;int eb=code%2048;int x=head;int z17=x%5+1;x/=5;int z13=x%5+1;x/=5;int z11=x%5+1;x/=5;int B7=x%5;x/=5;int A7=x%5;
    cout<<best<<" "<<A7<<" "<<B7<<" "<<z11<<" "<<z13<<" "<<z17<<" "<<eb<<"\n";
}
