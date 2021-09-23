$(document).ready(function() {
	$(chart_id).Highcharts.stockChart({
        rangeSelector: {selected: 1},
		chart: chart,
		title: title,
		xAxis: xAxis,
		yAxis: yAxis,
        series: series,
        credits: credits,
        legend: legend
	});
});