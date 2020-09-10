$(document).ready(function() {
	$(chart_id).highcharts({
		chart: chart,
		title: title,
		xAxis: xAxis,
		yAxis: yAxis,
        series: series,
        credits: {"enabled":"false"},
        legend: {"enabled":"false"}
	});
});