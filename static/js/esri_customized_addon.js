function LoadHeatmapImage(){

  // a new heatmap graphic layer
  // draw a picturefillsymble polygon

  let textend;
  let wholearea;
  if(activeWidget){
    textent=activeWidget.viewModel.measurement.geometry.extent;
    wholearea=activeWidget.viewModel.measurement.area;
  }
  else{
    jsonextent=view.extent.toJSON();
    textent=Extent.fromJSON(jsonextent);

    let ori_xmin=textent.xmin;
    let ori_wid=textent.width*0.01;

    textent=textent.expand(0.8);

    let centerpoint = textent.center.clone();
    centerpoint.x= textent.center.x-(textent.xmin-ori_xmin-ori_wid);
    textent=textent.centerAt(centerpoint);


    wholearea=geometryEngine.planarArea(Polygon.fromExtent(textent));
  }


  let lbx=textent.xmin,
      lby=textent.ymin,
      rtx=textent.xmax,
      rty=textent.ymax;
      gwidth=textent.width;
      gheight=textent.height;
      console.log(textent);

   const heatrings=[
       [rtx,rty],
       [rtx,lby],
       [lbx,lby],
       [lbx,rty],
       [rtx,rty]
     ];

   var fillSymbol = {
      type: "picture-fill", //"picture-fill" // autocasts as new PictureFillSymbol()

      //xscale: 40,
      //yscale: 40,
      height: "400px",//gheight.toString()+" px",
      width: "200px",//gwidth.toString()+" px",
      url: "{% static 'img/testheatmap.png' %}",
      outline: {
        style: "none"
      },
    };

    var fillSymbol2 = {
              type: "simple-fill", // autocasts as new SimpleFillSymbol()
              color: [227, 139, 79, 0.8],
              outline: {
                // autocasts as new SimpleLineSymbol()
                color: [255, 255, 255],
                width: 1
              }
            };

    var polygon = {
         type: "polygon", // autocasts as new Polygon()
         rings: heatrings,
         spatialReference:view.spatialReference
       };

   var polygonGraphic = new Graphic({
      geometry: polygon,
      symbol: fillSymbol
    });
     //console.log(polygonGraphic);
  // Add the graphics to the view's graphics layer
  graphicHeatmapLayer.addMany([polygonGraphic]);

}
