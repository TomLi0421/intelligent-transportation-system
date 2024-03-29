import "./App.css";
import DriverTable from "./components/DriverTable";
import LineChart from "./components/LineChart";

function App() {
  return (
    <div className="px-10 pt-12">
      <h1 className="mb-5 font-medium text-4xl">
        Intelligent Transportation System
      </h1>
      <DriverTable />
      <div className="mt-10">
        <LineChart />
      </div>
    </div>
  );
}

export default App;
