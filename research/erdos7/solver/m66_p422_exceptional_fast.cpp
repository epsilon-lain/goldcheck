// M66 exact exhaustive verifier for the exceptional P422 hard seed.
// Target: 3^4 * 5^2 * 7 * 11^2 * 13 * 17.
// Local non-special order is (11^2,7,13,17).
// Compile: g++ -O3 -fopenmp m66_p422_exceptional_fast.cpp -o m66_p422_exceptional_fast
// Expected output: 3404158 1 1 3 3 2 1127
// Compare against Q*C = 3402000 for C=1701/5000.

#include <bits/stdc++.h>
#include <omp.h>
using namespace std; using i128=__int128_t; using i64=long long;
struct Rat{long long n,d;};
static inline i64 floordiv(i128 a,i128 b){i128 q=a/b,r=a%b;if(r!=0&&a<0)--q;return(i64)q;}
const long long Q=10000000LL;
const int Dv[4]={121,7,13,17};
const int denv[16]={1,121,7,847,13,1573,91,11011,17,2057,119,14399,221,26741,1547,187187};
const int csv[16]={1,12,1,12,1,12,1,12,1,12,1,12,1,12,1,12};
const int lowv[16]={1,61,2,62,8,428,11,11,12,672,19,259,91,4291,77,-3943};
const int highv[16]={1,109,6,642,12,1296,71,7511,16,1732,95,10079,191,20471,1117,117049};
const Rat lam[16]={{0LL,1LL},{3LL,4LL},{247LL,1000LL},{169LL,200LL},{177LL,1000LL},{409LL,500LL},{347LL,500LL},{937LL,1000LL},{33LL,500LL},{831LL,1000LL},{173LL,250LL},{461LL,500LL},{87LL,125LL},{903LL,1000LL},{213LL,250LL},{541LL,500LL}};
const Rat nu[16]={{197LL,500LL},{113LL,1000LL},{428LL,125LL},{951LL,1000LL},{2233LL,500LL},{947LL,500LL},{10LL,1LL},{10LL,1LL},{6731LL,1000LL},{221LL,1000LL},{10LL,1LL},{10LL,1LL},{10LL,1LL},{10LL,1LL},{10LL,1LL},{10LL,1LL}};
const int LIN[15]={0,0,323,0,175,292,271,0,179,197,530,191,229,207,0};
const int CRS[105]={1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,5,5,5,5,5,5,5,5,5,5,6,6,6,6,6,6,6,6,6,7,7,7,7,7,7,7,7,8,8,8,8,8,8,8,9,9,9,9,9,9,10,10,10,10,10,11,11,11,11,12,12,12,13,13,14};
const int CRT[105]={2,3,4,5,6,7,8,9,10,11,12,13,14,15,3,4,5,6,7,8,9,10,11,12,13,14,15,4,5,6,7,8,9,10,11,12,13,14,15,5,6,7,8,9,10,11,12,13,14,15,6,7,8,9,10,11,12,13,14,15,7,8,9,10,11,12,13,14,15,8,9,10,11,12,13,14,15,9,10,11,12,13,14,15,10,11,12,13,14,15,11,12,13,14,15,12,13,14,15,13,14,15,14,15,15};
const int CR[105]={0,26,0,274,0,0,0,405,0,0,0,0,0,0,303,0,0,265,0,0,0,377,0,0,0,108,0,0,124,1,2096,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,221,7597,0,97,0,0,0,8000,6863,0,0,0,0,204,0,1067,0,1597,0,0,3173,3783,0,0,2047,0,0,0,0,0,54,0,0,0,0,0,0,0,0,0,0,450,0,7663,0,15,0,0,0,2292,0,130488,0,0,0};
const int FAC[10]={12,6,1,1,18,17,8,5,7,3};
const int ums[11]={3,5,6,7,9,10,11,12,13,14,15};
const i64 PCOORD=704992LL;
vector<i64> phiTab[16];
static inline i64 phi_floor(int C,int n){
 int T=15^C; Rat L=lam[T],N=nu[T];
 i128 a=(i128)L.n*denv[C]-(i128)n*L.d; i128 bb=(i128)L.d*denv[C];
 i128 xn=-a*N.d, xd=(i128)2*N.n*bb;
 i128 lon=(i128)6*csv[T], lod=(i128)25*denv[T], hin=5*lon,hid=lod;
 if(xn*lod<lon*xd){i128 xnum=lon,xden=lod; i128 num=(i128)N.n*xnum*xnum*bb+a*xnum*N.d*xden; i128 den=(i128)N.d*xden*xden*bb;return floordiv(num*Q,den);}
 if(xn*hid>hin*xd){i128 xnum=hin,xden=hid; i128 num=(i128)N.n*xnum*xnum*bb+a*xnum*N.d*xden; i128 den=(i128)N.d*xden*xden*bb;return floordiv(num*Q,den);}
 i128 num=-(i128)a*a*N.d*Q; i128 den=(i128)4*N.n*bb*bb; return floordiv(num,den);
}
static inline i64 rat_floor(long long n,long long d){return floordiv((i128)n*Q,d);}
static inline void rho_nums(int A0,int B0,int z1,int z2,int z3,int eb,long long n[16],long long t[16]){
 memset(t,0,16*sizeof(long long)); t[1]=12+11*A0+B0;t[2]=z1*1;t[4]=z2*1;t[8]=z3*1;
 for(int j=0;j<11;j++){int m=ums[j];int z=((eb>>j)&1)?5:1;t[m]=(long long)csv[m]*z;}
 memset(n,0,16*sizeof(long long));n[0]=1;
 for(int sz=1;sz<=4;sz++)for(int C=1;C<16;C++)if(__builtin_popcount((unsigned)C)==sz){
  int pivot=C&-C,i=__builtin_ctz((unsigned)pivot),rest=C^pivot; long long v=(long long)Dv[i]*n[rest];int T=rest;
  while(true){int S=pivot|T;v-=t[S]*n[C^S];if(T==0)break;T=(T-1)&rest;}n[C]=v;
 }
}
static inline i64 eval_state(int A0,int B0,int z1,int z2,int z3,int eb){
 long long n[16],t[16];rho_nums(A0,B0,z1,z2,z3,eb,n,t);
 i64 full=rat_floor(n[15],denv[15]);for(int C=0;C<16;C++)full+=phiTab[C][n[C]-lowv[C]];
 i64 mc=LLONG_MAX;for(int C=1;C<16;C++)mc=min(mc,rat_floor(n[C],denv[C]));
 i64 base=min(full,mc+PCOORD),feat=0;
 for(int m=1;m<16;m++){int c=LIN[m-1];if(c)feat+=floordiv((i128)c*t[m]*Q,(i128)1000*denv[m]);}
 for(int k=0;k<105;k++){int c=CR[k];if(c)feat+=floordiv((i128)c*t[CRS[k]]*t[CRT[k]]*Q,(i128)1000*denv[CRS[k]]*denv[CRT[k]]);}
 int acts[5]={A0,B0,z1-1,z2-1,z3-1};long long units=0;
 for(int j=0;j<5;j++){int A=acts[j];units+=(long long)FAC[2*j]*A+(long long)FAC[2*j+1]*(A*(A-1)/2);}feat+=units*(Q/1000);
 return base+feat;
}
int main(){
 for(int C=0;C<16;C++){phiTab[C].resize(highv[C]-lowv[C]+1);for(int n=lowv[C];n<=highv[C];n++)phiTab[C][n-lowv[C]]=phi_floor(C,n);}
 i64 best=LLONG_MAX;long long code=-1;
 #pragma omp parallel
 {
  i64 lb=LLONG_MAX;long long lc=-1;
  #pragma omp for schedule(static)
  for(int head=0;head<3125;head++){int x=head;int z3=x%5+1;x/=5;int z2=x%5+1;x/=5;int z1=x%5+1;x/=5;int B0=x%5;x/=5;int A0=x%5;
   for(int eb=0;eb<2048;eb++){i64 v=eval_state(A0,B0,z1,z2,z3,eb);if(v<lb){lb=v;lc=(long long)head*2048+eb;}}
  }
  #pragma omp critical
  if(lb<best){best=lb;code=lc;}
 }
 long long head=code/2048;int eb=code%2048;int x=head;int z3=x%5+1;x/=5;int z2=x%5+1;x/=5;int z1=x%5+1;x/=5;int B0=x%5;x/=5;int A0=x%5;
 cout<<best<<" "<<A0<<" "<<B0<<" "<<z1<<" "<<z2<<" "<<z3<<" "<<eb<<"\n";
}
