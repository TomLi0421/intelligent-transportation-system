import React from "react";

function OverspeedHistoryCard({ driverId, time, speed }) {
  return (
    <div className="bg-slate-50 rounded-md py-8 px-7 flex justify-between items-baseline mb-5">
      <div>
        <h2 className="text-black text-sm md:text-xl font-medium">
          {driverId}
        </h2>
        <h4 className="text-slate-500 font-normal text-sm">{time}</h4>
      </div>
      <div>
        <h2 className="text-right">
          <span className="text-sm md:text-xl font-medium text-red-600 ">
            {speed}
          </span>{" "}
          km/h
        </h2>
        <h4 className="text-slate-500 font-normal text-sm text-right">Speed</h4>
      </div>
    </div>
  );
}

export default OverspeedHistoryCard;
