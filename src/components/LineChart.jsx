import React, { useState, useEffect } from "react";
import { generateDummyData } from "../data/CHART_DATA";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

function LineChart({ dummy_chartData }) {
  const [chartData, setChartData] = useState(generateDummyData(10, 1));

  useEffect(() => {}, []);

  const colors = [
    "#FF0000",
    "#00FF00",
    "#0000FF",
    "#FFFF00",
    "#FF00FF",
    "#00FFFF",
    "#000000",
    "#800000",
    "#008000",
    "#000080",
  ];
  return <>{/* <Line options={options} data={data} /> */}</>;
}

export default LineChart;

// text: "Real time driving Speed Monitoring",
