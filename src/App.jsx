import "./App.css";
import DriverTable from "./components/DriverTable";
import LineChart from "./components/LineChart";
import OverspeedList from "./components/OverspeedHistory/OverspeedHistoryList";

function App() {
  return (
    <div className="px-10 py-12">
      <h1 className="mb-5 font-medium text-4xl">
        Intelligent Transportation System
      </h1>

      <DriverTable />

      <div className="grid grid-cols-3 gap-x-10 mt-10">
        <LineChart />
        <OverspeedList />
      </div>
    </div>
  );
}

export default App;
