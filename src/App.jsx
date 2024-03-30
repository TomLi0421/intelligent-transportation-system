import "./App.css";
import DriverTable from "./components/DriverTable";
import LineChart from "./components/LineChart";
import OverSpeedHistory from "./components/OverSpeedHistoryCard";
import summaryData from "./data/SUMMARY_DATA";
import dummy_chartData from "./data/CHART_DATA";

function App() {
  return (
    <div className="px-10 pt-12">
      <h1 className="mb-5 font-medium text-4xl">
        Intelligent Transportation System
      </h1>
      <DriverTable summaryData={summaryData} />
      <div className="grid grid-cols-3 gap-x-10">
        <div className="bg-white p-8 rounded-lg my-10 col-span-2">
          <LineChart dummy_chartData={dummy_chartData} />
        </div>
        <div className="bg-white p-8 rounded-lg my-10 ">
          <OverSpeedHistory />
        </div>
      </div>
    </div>
  );
}

export default App;
