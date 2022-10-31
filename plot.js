let titles = [];
let comment_counts = [];
let episode_number = [];
let infos = [];

Papa.parse("./episode_infos.csv", {
  download: true,
  header: true,
  dynamicTyping: true,
  complete: function (results) {
    //     console.log(results.data);
    for (let i = 0; i < results.data.length; i++) {
      infos.push(results.data[i]);
      titles.push(results.data[i]["titles"]);
      if (results.data[i]["comment_count"] == undefined) {
        results.data[i]["comment_count"] = 0;
      }
      comment_counts.push(results.data[i]["comment_count"]);
      episode_number.push(results.data[i]["episode_numbers"]);
    }
  },
});

setTimeout(function () {
  let columns = {
    titles: "interval",
    comment_count: "interval",
    episode_numbers: "interval",
  };
  let stats = new Statistics(infos, columns);
  let mean = stats.arithmeticMean("comment_count");
  let median = stats.median("comment_count");
  let stdDev = stats.standardDeviation("comment_count");

  console.log(comment_counts);

  document.getElementById("Mittelwert").innerText =
    "Mittelwert: " + String(mean);
  document.getElementById("Median").innerText = "Median: " + String(median);
  document.getElementById("Standardabweichung").innerText =
    "Standardabweichung: " + String(stdDev);

  PLOT_AREA1 = document.getElementById("plotArea1");
  PLOT_AREA2 = document.getElementById("plotArea2");

  Plotly.newPlot(
    PLOT_AREA1,
    [
      {
        x: episode_number,
        y: comment_counts,
        text: titles,
        type: "bar",
        marker: {
          color: "rgb(158,0,209)",
        },
      },
    ],
    {
      margin: { t: 200 },
      showlegend: false,
      bargap: 0.2,
      title: "Kommentare pro Episode",
      xaxis: { title: "Episoden Nummer" },
      yaxis: { title: "Kommentar Anzahl" },
    }
  );

  Plotly.newPlot(
    PLOT_AREA2,
    [
      {
        x: comment_counts,
        type: "histogram",
        xbins: {
          size: 1,
        },
        marker: {
          color: "rgb(158,0,209)",
        },
      },
    ],
    {
      margin: { t: 200 },
      showlegend: false,
      bargap: 0.05,
      title: "Auftreten der Kommentar Anzahlen",
      xaxis: { title: "Kommentar Anzahl" },
      yaxis: { title: "Anzahl aufgetreten" },
    }
  );
}, 1000);
