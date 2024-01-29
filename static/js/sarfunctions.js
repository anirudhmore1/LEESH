function hslToRgb(h, s, l) {
    var r, g, b;

     if (s == 0) {
         r = g = b = l; // achromatic
     } else {
         function hue2rgb(p, q, t) {
             if (t < 0) t += 1;
             if (t > 1) t -= 1;
             if (t < 1 / 6) return p + (q - p) * 6 * t;
             if (t < 1 / 2) return q;
             if (t < 2 / 3) return p + (q - p) * (2 / 3 - t) * 6;
             return p;
         }

         var q = l < 0.5 ? l * (1 + s) : l + s - l * s;
         var p = 2 * l - q;
         r = hue2rgb(p, q, h + 1 / 3);
         g = hue2rgb(p, q, h);
         b = hue2rgb(p, q, h - 1 / 3);
     }
     return [r * 255, g * 255, b * 255];
 }

 function ColorGroupInitialize(){
   let t_colorgroup={};
   t_colorgroup['line1']=[getRandomInt(255), getRandomInt(255), getRandomInt(255)];
   t_colorgroup['line2']=[getRandomInt(255), getRandomInt(255), getRandomInt(255)];

   t_colorgroup['drone1']=[getRandomInt(255), getRandomInt(255), getRandomInt(255)];
   t_colorgroup['drone2']=[getRandomInt(255), getRandomInt(255), getRandomInt(255)];

   t_colorgroup['path1']=[getRandomInt(255), getRandomInt(255), getRandomInt(255)];
   t_colorgroup['path2']=[getRandomInt(255), getRandomInt(255), getRandomInt(255)];
   return t_colorgroup;
 }

 function getRandomInt(max) {
   return Math.floor(Math.random() * Math.floor(max));
 }

 function download(filename, text) {
   var element = document.createElement('a');
   element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
   element.setAttribute('download', filename);

   element.style.display = 'none';
   document.body.appendChild(element);

   element.click();

   document.body.removeChild(element);
 }

 function ContourRingdownload(in_rings,index=0){
   // 20200723 tian start test
   // target: use python to generate contour map images
   // download the rings to a document
   console.log(in_rings);
   str_ring=JSON.stringify(in_rings);
   let filename="Ring"+"_"+index.toString()+".txt";
   download(filename, str_ring);
 }

 function polygonClone(polygon) {
   let cloned = [],
       i,
       n;

   for (i = 0, n = polygon.length; i < n; i++) {
     cloned.push([polygon[i][0], polygon[i][1]]);
   }

   return cloned;
 }


function FilterBoundary(x,y,maxx,maxy,minx,miny){
  if (x>maxx) {
   x=maxx;
  }
  else if (x<minx) {
   x=minx;
  }
  if (y>maxy) {
   y=maxy;
  }
  else if (y<miny) {
   y=miny;
  }
  return [x,y];
}

function GetObjectLength(object){
  var length = 0;
    for( var key in object ) {
        if( object.hasOwnProperty(key) ) {
            ++length;
        }
    }
    return length;
}

var m_clue_template = {
    title: "{Name}",
    content: [
      {
        type: "fields",
        fieldInfos: [{fieldName: "Name"},{fieldName: "LostHour"}]
      }
    ]
};

function GetSites(n,t_extent){
  let res_points=[];
  //center point [0,0]
  //first round radius:1, second:2,third:3
  let t_radius=1;
  let t_firstround=6;

  //second round
  let res_count=0;
  let t_wholearea=0;
  let t_cellarea=t_radius*t_radius/t_firstround;

  while(n>res_count){
    let t_roundarea=t_radius*t_radius-t_wholearea;
    let t_celldegree=t_cellarea/t_roundarea;
    let t_totaldegree=0;
    while(t_totaldegree<=0.99){
      res_points.push([(t_radius-0.5)*Math.sin(2*Math.PI*t_totaldegree),(t_radius-0.5)*Math.cos(2*Math.PI*t_totaldegree)]);
      t_totaldegree=t_totaldegree+t_celldegree;
      res_count=res_count+1;
    }
    t_wholearea=t_radius*t_radius;
    t_radius=t_radius+1;
  }

  //standrized from 1:1 into width and height ratio
  t_radius=t_radius-1;
  let t_wscale=t_extent.width/(2*t_radius);
  let t_hscale=t_extent.height/(2*t_radius);

  for(let i=0;i<res_count;i++){
    res_points[i][0]=res_points[i][0]*t_wscale+t_extent.center.x;
    res_points[i][1]=res_points[i][1]*t_hscale+t_extent.center.y;
  }
  return res_points;
}

//sites = GetSites(npoints,textent);
function GetSites3(n,t_extent){
  let res_points=[];
  //center point [0,0]
  //first round radius:1, second:2,third:3
  let t_radius=1;
  let t_firstround=6;

  //second round
  let res_count=0;
  let t_wholearea=0;
  let t_cellarea=t_radius*t_radius/t_firstround;

  while(res_count<n){
    let t_roundarea=t_radius*t_radius-t_wholearea;
    let t_celldegree=t_cellarea/t_roundarea;
    let t_totaldegree=0;
      
    let t_arr=[];
    let t_count=0;
    while(t_totaldegree<=0.99){
      t_arr.push([(t_radius-0.5)*Math.sin(2*Math.PI*t_totaldegree),(t_radius-0.5)*Math.cos(2*Math.PI*t_totaldegree)]);
      t_totaldegree=t_totaldegree+t_celldegree;
      t_count=t_count+1;
    }
      
    if(res_count+t_count<=n){
        res_points=res_points.concat(t_arr);
        res_count=res_count+t_count;
    }
    else{
        let subdeg=1/(n-res_count+3);
        for(let i=0;i<n-res_count+3;++i){
            res_points.push([(t_radius-0.5)*Math.sin(2*Math.PI*subdeg*i),(t_radius-0.5)*Math.cos(2*Math.PI*subdeg*i)]);
        }
        res_count=n+3;        
    }
    
    t_wholearea=t_radius*t_radius;
    t_radius=t_radius+1;
  }

  //standrized from 1:1 into width and height ratio
  t_radius=t_radius-1;
  let t_wscale=t_extent.width/(2*t_radius);
  let t_hscale=t_extent.height/(2*t_radius);

  for(let i=0;i<res_count;i++){
    res_points[i][0]=res_points[i][0]*t_wscale+t_extent.center.x;
    res_points[i][1]=res_points[i][1]*t_hscale+t_extent.center.y;
  }
  return res_points;
}


//sites = GetSites(npoints,textent);
function GetSites4(n,t_extent){
    let res_points=[];
    //center point [0,0]
    //first round radius:1, second:2,third:3
    // area: 1: 3: 5:7:9

    let t_firstround=6;
    let arr=[];
    let i=0;
    let npt=0;
    let minout=3;
    while(npt<n){
        let ncircle=2*i+1;
        
        if(npt+ncircle*t_firstround<=n){
            arr.push(ncircle*t_firstround);
            npt = npt+ncircle*t_firstround;
        }
        else{
            arr.push(n-npt+minout);
            npt = n+minout;
        }
        ++i;
    }
    //console.log(n,arr);
    let tr=0.5;//0.5;
    for(i=0;i<arr.length;++i){
        let subdeg=1/arr[i];
        for(let j=0;j<arr[i];++j){
            let tsin=Math.sin(2*Math.PI*subdeg*j);
            //res_points.push([(i+tr)*Math.sin(2*Math.PI*subdeg*j),(i+tr)*Math.cos(2*Math.PI*subdeg*j)]);
            res_points.push([(i+tr*(tsin+0.5))*tsin,(i+tr*(tsin+0.5))*Math.cos(2*Math.PI*subdeg*j)]);
        }        
    }
    
    //standrized from 1:1 into width and height ratio
    let t_wscale=t_extent.width/(2*arr.length);
    let t_hscale=t_extent.height/(2*arr.length);

    for(let i=0;i<res_points.length;i++){
        res_points[i][0]=res_points[i][0]*t_wscale+t_extent.center.x;
        res_points[i][1]=res_points[i][1]*t_hscale+t_extent.center.y;
    }
    //console.log(res_points);
    return res_points;
    
}