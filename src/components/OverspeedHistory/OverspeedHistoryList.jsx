import React from "react";
import OverspeedHistoryCard from "./OverspeedHistoryCard";

function OverspeedHistoryList() {
  return (
    <div className="bg-white p-8 rounded-lg">
      <h2 className="font-medium text-xl mb-5">Overspeed History</h2>
      <OverspeedHistoryCard />
    </div>
  );
}

export default OverspeedHistoryList;
