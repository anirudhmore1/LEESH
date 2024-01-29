
function DrawRigs() {
  //document.body.style.background="url('static/img/bg.jpg')";
  //$('#bgimg').css("background-image","url('img/testmap.png')");
  
  var nn=Math.floor(document.getElementById("areapoints").value);
  //var ppl=document.getElementById("segmentpoints").value;
  //document.getElementById("test1").value=ppl;
  var ppl=Math.floor(document.getElementById("segmentpoints").value);

  //var nn=3;
  //var ppl=2;

  var n =(nn-1)*(1+ppl)+1;
  var canvas = document.querySelector("canvas");

  var context = canvas.getContext("2d"),
      width = canvas.width,
      height = canvas.height,
      p_width=0.9*Math.min(canvas.width,canvas.height) /n;

  //var img = document.getElementById("testmap");
  //context.drawImage(img, 10, 10);


  if(ppl<=0){
    ppl=1;
  }

  var nodes = d3.range(n * n).map(function(i) {
    return {
      index: i,
      fx : (i%n-n/2)*p_width,
      fy : (Math.floor(i/n)-n/2)*p_width
    };
  });



  for  (var x = 0; x < n; x++) {
    for (var y = 0; y < n; y++){
      if(x%(ppl+1)>0.99 && y%(ppl+1)>0.99){
        nodes[x*n+y].fx=width;
        nodes[x*n+y].fy=height;
      }
    }
  }
  //console.log(nodes)

  var links = [];
  for (var y = 0; y < n; ++y) {
    for (var x = 0; x < n; ++x) {
        if (y > 0 && x%(ppl+1)<0.0000001) links.push({source: (y - 1) * n + x, target: y * n + x});
        if (x > 0 && y%(ppl+1)<0.0000001) links.push({source: y * n + (x - 1), target: y * n + x});

    }
  }
  var simulation = d3.forceSimulation(nodes)
      .force("charge", d3.forceManyBody().strength(0))
      .force("link", d3.forceLink(links).strength(1).distance(10).iterations(10))
      .on("tick", ticked);




  d3.select(canvas)
      .call(d3.drag()
          .container(canvas)
          .subject(dragsubject)
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended));

  function ticked() {
    context.clearRect(0, 0, width, height);
    context.save();
    context.translate(width / 2, height / 2);

    context.beginPath();
    links.forEach(drawLink);
    context.strokeStyle = "#aaa";
    context.stroke();

    context.beginPath();
    nodes.forEach(drawNode);
    context.fill();
    context.strokeStyle = "#fff";
    context.stroke();

    context.restore();
  }

  function dragsubject() {
    return simulation.find(d3.event.x - width / 2, d3.event.y - height / 2);
  }

  function dragstarted() {
    if (!d3.event.active) simulation.alphaTarget(0.3).restart();
    d3.event.subject.fx = d3.event.subject.x;
    d3.event.subject.fy = d3.event.subject.y;
  }

  function dragged() {
    d3.event.subject.fx= Math.max(-width/2,Math.min(width/2, d3.event.x));
    d3.event.subject.fy =  Math.max(-height/2,Math.min(height/2, d3.event.y));
    //d3.event.subject.fx = d3.event.x;
    //d3.event.subject.fy = d3.event.y;
  }

  function dragended() {
    if (!d3.event.active) simulation.alphaTarget(0);

    //d3.event.subject.fx = null;
    //d3.event.subject.fy = null;
  }

  function drawLink(d) {
    context.moveTo(d.source.x, d.source.y);
    context.lineTo(d.target.x, d.target.y);
  }

  function drawNode(d) {
    context.moveTo(d.x + 3, d.y);
    context.arc(d.x, d.y, 3, 0, 2 * Math.PI);
  }
}
