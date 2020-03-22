d3.csv("archive.csv").then(data =>{
    data.forEach(d => {
        d.Datum = d.retrieval_time;
        d.BW = +d.BW;
        d.BY = +d.BY;
        d.BE = +d.BE;
        d.BB = +d.BB;
        d.HB = +d.HB;
        d.HH = +d.HH;
        d.HE = +d.HE;
        d.MV = +d.MV;
        d.NI = +d.NI;
        d.NW = +d.NW;
        d.RP = +d.RP;
        d.SL = d.SL;
        d.SN = +d.SN;
        d.ST = +d.ST;
        d.SH = +d.SH;
        d.TH = +d.TH;
        d.total = d.total;
    });
    displayTable(data);
});

function displayTable(data) {
    var table = d3.select('table')
    var thead = table.append('thead')
    var tbody = table.append('tbody')

    thead.append('tr')
        .selectAll('th')
        .data(data.columns)
        .enter()
        .append('th')
        .text(function (d) {
            return d
        })
    var rows = tbody.selectAll('tr')
        .data(data)
        .enter()
        .append('tr')

    var cells = rows.selectAll('td')
        .data(function (row) {
            return data.columns.map(function (column) {
                return {
                    column: column,
                    value: row[column]
                }
            })
        })
        .enter()
        .append('td')
        .text(function (d) {
            return d.value
        })
    return table;
};