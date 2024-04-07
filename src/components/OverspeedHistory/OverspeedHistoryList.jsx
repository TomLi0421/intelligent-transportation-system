import OverspeedHistoryCard from "./OverspeedHistoryCard";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

function OverspeedHistoryList({ driverData }) {
  const overspeedData = driverData.filter((driver) => driver.IsOverspeed === 1);

  if (overspeedData) {
    overspeedData.map((driver) =>
      toast.error(`${driver.DriverID} is overspeed`, {
        position: "top-right",
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
        theme: "light",
      })
    );
  }

  return (
    <div className="overflow-auto max-h-[38rem]">
      {overspeedData.map((driver, index) => (
        <OverspeedHistoryCard
          key={index}
          driverId={driver.DriverID}
          time={driver.CurrentTime}
          speed={driver.Speed}
        />
      ))}
      <ToastContainer />
    </div>
  );
}

export default OverspeedHistoryList;
