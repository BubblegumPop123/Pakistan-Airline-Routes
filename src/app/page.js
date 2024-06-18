"use client";

import React, { useEffect, useState } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import axios from "axios";

export default function Home() {
  const [startDate, setStartDate] = useState(new Date());
  const [Loading, setLoading] = useState(false);
  const [Data, setData] = useState("");
  const [Source, setSource] = useState("");
  const [Destination, setDestination] = useState("");

  // useEffect(() => {
  //   const fetchData = async () => {
  //     setLoading(true);
  //     const Data = new FormData();
  //     Data.append("SourceCity", "Islamabad");
  //     Data.append("DestinationCity", "Karachi");
  //     Data.append("Date", "2021-10-10");
  //     const result = await axios.post("http://127.0.0.1:8000/getPath", Data);
  //     setData(result);
  //     setLoading(false);
  //   };
  //   fetchData();
  // }, []);

  const HandelClick = async () => {
    setLoading(true);

    var dateObject = new Date(startDate);

    // Extract year, month, and day from the Date object
    var year = dateObject.getFullYear();
    var month = (dateObject.getMonth() + 1).toString().padStart(2, "0"); // Add 1 to the month because it's 0-indexed
    var day = dateObject.getDate().toString().padStart(2, "0");

    // Create the output date string in the "YYYY-MM-DD" format
    var outputDateString = `${year}-${month}-${day}`;
    const Data = new FormData();
    Data.append("SourceCity", Source);
    Data.append("DestinationCity", Destination);
    Data.append("Date", outputDateString);
    const result = await axios.post("http://127.0.0.1:8000/getPath", Data);
    console.log(result.data);
    setData(result.data);
    setLoading(false);
  };

  return (
    <div className="bg-gray-200 p-20">
      <h1 className="text-4xl font-extrabold text-center">
        Optimal Route for Aircraft
      </h1>
      <div className="grid grid-cols-2 gap-10 mt-10">
        <div className="border-[3px] bg-white border-black rounded-lg p-10 flex flex-col justify-center items-center">
          <div className="w-full">
            <label
              for="countries"
              className="block text-xl mb-2 font-medium text-gray-900 dark:text-white"
            >
              Choose Source Airport
            </label>
            <select
              onChange={(e) => setSource(e.target.value)}
              id="countries"
              class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            >
              <option selected>Choose Source Airport</option>
              <option value="Islamabad">Islamabad</option>
              <option value="Karachi">Karachi</option>
              <option value="Lahore">Lahore</option>
              <option value="Peshawar">Peshawar</option>
              <option value="Quetta">Quetta</option>
              <option value="Multan">Multan</option>
              <option value="Faisalabad">Faisalabad</option>
              <option value="Rawalpindi">Rawalpindi</option>
              <option value="Sialkot">Sialkot</option>
              <option value="Gujranwala">Gujranwala</option>
              <option value="Sukkur">Sukkur</option>
              <option value="Gwadar">Gwadar</option>
            </select>
          </div>
          <div className="mt-10 w-full">
            <label
              for="Destination"
              className="block text-xl mb-2 font-medium text-gray-900 dark:text-white"
            >
              Choose Destination Airport
            </label>
            <select
              onChange={(e) => setDestination(e.target.value)}
              id="Destination"
              class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            >
              <option selected>Choose Source Airport</option>
              <option value="Islamabad">Islamabad</option>
              <option value="Karachi">Karachi</option>
              <option value="Lahore">Lahore</option>
              <option value="Peshawar">Peshawar</option>
              <option value="Quetta">Quetta</option>
              <option value="Multan">Multan</option>
              <option value="Faisalabad">Faisalabad</option>
              <option value="Rawalpindi">Rawalpindi</option>
              <option value="Sialkot">Sialkot</option>
              <option value="Gujranwala">Gujranwala</option>
              <option value="Sukkur">Sukkur</option>
              <option value="Gwadar">Gwadar</option>
            </select>
          </div>
          <div className="w-full mt-10 ">
            <h1 className="text-xl mb-2 font-medium text-gray-900 dark:text-white">
              Set The Date of Your Flight
            </h1>
            <DatePicker
              className="border border-black rounded-lg pl-3 pr-3 mt-1 "
              selected={startDate}
              onChange={(date) => setStartDate(date)}
            />
          </div>
          <button
            onClick={HandelClick}
            className="mt-10 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          >
            {Loading ? (
              <div role="status">
                <svg
                  aria-hidden="true"
                  class="w-8 h-8 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600"
                  viewBox="0 0 100 101"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                    fill="currentColor"
                  />
                  <path
                    d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                    fill="currentFill"
                  />
                </svg>
                <span class="sr-only">Loading...</span>
              </div>
            ) : (
              "Get The Optimal Route"
            )}
          </button>
        </div>
        <div className="flex flex-col justify-center items-center ">
          <h1 className="text-2xl font-bold">The Optimal Route</h1>
          <div className="h-full w-full flex justify-center items-center">
            {Loading ? (
              <div role="status">
                <svg
                  aria-hidden="true"
                  class="w-8 h-8 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600"
                  viewBox="0 0 100 101"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                    fill="currentColor"
                  />
                  <path
                    d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                    fill="currentFill"
                  />
                </svg>
                <span class="sr-only">Loading...</span>
              </div>
            ) : (
              <h1>{Data}</h1>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
