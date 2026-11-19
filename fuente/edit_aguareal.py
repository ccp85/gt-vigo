# Agua más realista en todo el mar de GT Vigo (index, indexm, gp, nav, navm).
# Sustituye aguaSamil(): en vez de dos manchas de ruido azul, el mar es ahora
#  - oleaje de verdad: suma de 8 trenes de olas (senos de cresta aguda) con la dispersión real del agua
#    (las largas, mar de fondo del Atlántico entrando por la ría, van más rápido que las cortas);
#    las olas que salen más pequeñas que un par de píxeles se apagan solas (sin parpadeo en la vista de maqueta)
#  - rizos finos de viento con «calmas» (manchas lisas que se desplazan, como se ven desde el Castro)
#  - color por profundidad: azul petróleo oscuro en la ría, verde turquesa en lo poco hondo y arena bajo el agua en las playas
#  - reflejo del cielo (Fresnel) con los colores del cielo de cada hora y camino de destellos del sol (naranja al atardecer)
#  - espuma de rompiente que llega a la orilla y borreguillos mar adentro
# En el móvil (window.LITE) usa 5 trenes de olas y sin rizos finos.
import sys,os
# sin argumentos (cadena de build.sh): las cinco páginas generadas que haya en la carpeta
FILES=sys.argv[1:] or [f for f in ['index.html','indexm.html','gp.html','nav.html','navm.html'] if os.path.exists(f)]
NUEVO=r'''function aguaSamil(m){m.roughness=.6;m.metalness=.0;if(window.LITE)m.defines=Object.assign(m.defines||{},{AGUA_LITE:''});m.onBeforeCompile=sh=>{Object.assign(sh.uniforms,UW,UCO,{uSun:SKYU.uSun,uZen:SKYU.uZen,uHor:SKYU.uHor});
 sh.vertexShader='varying vec3 vWp;\n'+sh.vertexShader.replace('#include <begin_vertex>','#include <begin_vertex>\nvWp=(modelMatrix*vec4(position,1.0)).xyz;');
 sh.fragmentShader='uniform float uT;uniform float uN;uniform sampler2D uCos;uniform vec4 uCoR;uniform vec3 uSun,uZen,uHor;varying vec3 vWp;vec3 aN;float aF;\n'+
 '#ifdef AGUA_LITE\n#define NOLAS 5\n#else\n#define NOLAS 8\n#endif\n'+
 'float h21(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}\n'+
 'float vn(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(h21(i),h21(i+vec2(1,0)),f.x),mix(h21(i+vec2(0,1)),h21(i+vec2(1,1)),f.x),f.y);}\n'+
 // oleaje: x = altura relativa (0 valle … 1 cresta), yz = pendiente; 1 unidad ≈ 100 m, g = 0.098 u/s²
 'vec3 olas(vec2 p,float t,float fw,float calma,float aw){vec3 r=vec3(0.);float ang=.22,L=1.15,sa=0.;float wp=vn(p*.45+t*.01)*2.-1.;\n'+
 ' for(int i=0;i<NOLAS;i++){vec2 d=vec2(cos(ang),sin(ang));float k=6.2832/L;float w=sqrt(.098*k)*1.15;\n'+
 '  float A=.075/k*smoothstep(2.,6.,L/fw)*(i>2?mix(.3,1.,calma):1.)*mix(.35,1.,aw);\n'+
 '  float ph=dot(d,p)*k-w*t+float(i)*1.7+wp*(1.2+float(i)*.35);A*=.55+.9*vn(p*(.6+float(i)*.4)+float(i)*3.1);float e=exp(sin(ph)-1.);r.x+=A*e;r.yz+=A*e*cos(ph)*k*d;sa+=A;\n'+
 '  ang+=2.39996;L*=.66;}\n'+
 ' r.x=sa>0.?r.x/sa:0.;return r;}\n'+
 'float costa(){vec2 uv=(vWp.xz-uCoR.xy)/uCoR.zw;if(uv.x<0.||uv.y<0.||uv.x>1.||uv.y>1.)return 0.;return texture2D(uCos,uv).r;}\nfloat ancho(){vec2 uv=(vWp.xz-uCoR.xy)/uCoR.zw;if(uv.x<0.||uv.y<0.||uv.x>1.||uv.y>1.)return 1.;return texture2D(uCos,uv).g;}\n'+
 sh.fragmentShader.replace('#include <color_fragment>',`#include <color_fragment>
  vec2 p=vWp.xz;float cs=costa();float aw=ancho()*(1.-smoothstep(.985,.999,cs));   // agua que el mapa da por tierra (charcas): sin espuma
  float fw=max(length(fwidth(p)),1e-5);
  float calma=smoothstep(.3,.75,vn(p*.35+vec2(uT*.012,-uT*.008)));             // calmas: manchas lisas que deriva el viento
  vec3 O=olas(p,uT,fw,calma,aw);vec2 gr=O.yz;
  #ifndef AGUA_LITE
  {float rz=mix(.25,1.,calma)*smoothstep(1.5,5.,.045/fw);if(rz>.001){vec2 q=p*45.+vec2(uT*.9,-uT*.6);float e=.35,n0=vn(q),nx=vn(q+vec2(e,0.)),nz=vn(q+vec2(0.,e));gr+=vec2(nx-n0,nz-n0)/e*45.*.0016*rz;}}
  #endif
  aN=normalize(vec3(-gr.x,1.,-gr.y));
  float prof=1.-smoothstep(.12,.8,cs);                                             // 1 = ría honda, 0 = orilla
  vec3 deep=vec3(.008,.042,.072),mid=vec3(.012,.080,.100),shal=vec3(.030,.200,.195),arena=vec3(.13,.36,.29);
  float big=vn(p*.12+uT*.004);
  vec3 col=mix(mid,deep,smoothstep(.0,.6,prof)*(.7+.3*big));
  col=mix(col,shal,smoothstep(.3,.7,cs));col=mix(col,arena,smoothstep(.7,.9,cs)*aw);
  col=mix(col,vec3(.04,.10,.09),(1.-aw)*.6);                                      // dársenas y charcas: agua más turbia
  col+=vec3(.0,.018,.016)*smoothstep(.6,.95,O.x)*(1.-uN);                            // la luz atraviesa las crestas (verde)
  float fb=sin(cs*34.0-uT*1.6+vn(p*4.0)*4.0);
  float tx=smoothstep(.15,.6,vn(p*20.+uT*vec2(.35,-.2))*.6+vn(p*52.-uT*.3)*.4+.1);
  float foam=(smoothstep(.86,.975,cs)+smoothstep(.74,.94,cs)*smoothstep(.65,.97,fb)*.7)*tx*aw;
  float whc=smoothstep(.9,.99,O.x)*smoothstep(.72,.9,vn(p*1.3+uT*vec2(.1,.04)))*smoothstep(.5,.8,vn(p*7.+uT*.2))*(1.-calma)*prof*.45;   // borreguillos mar adentro
  aF=clamp(foam+whc*tx,0.,1.);
  col=mix(col,vec3(.78,.82,.84),aF*(1.0-uN*.6));
  diffuseColor.rgb=col;`).replace('#include <normal_fragment_maps>',`#include <normal_fragment_maps>
  normal=normalize((viewMatrix*vec4(normalize(mix(aN,vec3(0.,1.,0.),aF*.8)),0.)).xyz);`).replace('#include <opaque_fragment>',`{vec3 N=normalize(mix(aN,vec3(0.,1.,0.),aF));vec3 V=normalize(cameraPosition-vWp);float nv=max(dot(N,V),0.);
   vec3 Rf=reflect(-V,N);Rf.y=abs(Rf.y);
   vec3 sky=mix(uHor,uZen,.35+.65*smoothstep(.0,.5,Rf.y))*.82;
   float F=min((.02+.98*pow(1.-nv,5.))*1.2+.07+.06*calma,.58)*(1.-aF);                    // reflejo del cielo (Fresnel)
   outgoingLight=mix(outgoingLight,sky,F);
   vec3 Ls=normalize(uSun);float sd=max(dot(Rf,Ls),0.);float up=smoothstep(-.02,.12,Ls.y)*(1.-uN);
   vec3 sc=mix(vec3(1.,.5,.25),vec3(1.,.95,.86),smoothstep(.05,.4,Ls.y));
   outgoingLight+=sc*(pow(sd,700.)*10.+pow(sd,60.)*.35)*up*(1.-aF);}               // destellos y camino del sol
  #include <opaque_fragment>`)};m.needsUpdate=true}
'''
for f in FILES:
    s=open(f,encoding='utf-8').read()
    a=s.find('function aguaSamil(m){');b=s.find('\nfunction texturaCosta()',a)
    assert a>0 and b>a and s.count('function aguaSamil(m){')==1,(f,a,b)
    if 'NOLAS' in s[a:b]:print('ya estaba',f);continue
    s=s[:a]+NUEVO.strip('\n')+s[b:]
    open(f,'w',encoding='utf-8').write(s);print('ok aguareal',f)
