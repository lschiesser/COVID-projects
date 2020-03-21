d3.csv("data.csv").then(function(data){
  displayTL(data);
});

 function displayTL(data){
 	var table = "";
 	for(i=0;i<data.length;i++){
 		var row = data[i];
    if (i % 2 == 0){
      table += "<div class='container left'>";
      table += "<div class='content'>";
      table += "<h2>";
      table += row['date'];
      table += "</h2>";
      table += "<p>";
      table += row['text'];
      table += "</p>";
      table += "</div>";
      table += "</div>";
    } else {
      table += "<div class='container right'>";
      table += "<div class='content'>";
      table += "<h2>";
      table += row['date'];
      table += "</h2>";
      table += "<p>";
      table += row['text'];
      table += "</p>";
      table += "</div>";
      table += "</div>";
    }
 	$("#t").html(table);
  };
};
