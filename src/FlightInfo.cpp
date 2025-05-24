#include <iostream>
#include <vector>
#include <stdexcept>
#include <limits>

// Admittedly: First result on google for a c++ JSON library
#include <fstream>
#include <nlohmann/json.hpp> 
using json = nlohmann::json;

// Promt the user for a single parameter.
double getParameter(std::string promt) {
  std::cout << promt;
  double result;
  std::cin >> result;
  // Ensure input was valid, otherwise clear cin and throw error.
  if (std::cin.fail()) {
    std::cin.clear();
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    throw std::invalid_argument("Invalid input, not a number.");
  }
  return result;
}

// Retrieve the 4 parameters asked for.
std::array<double, 4> getParameters() {
  std::array<double, 4> result;
  result[0] = getParameter("Please enter distance in NM: ");
  result[1] = getParameter("Please enter weight in lbs.: ");
  result[2] = getParameter("Please enter altitude in feet: ");
  result[3] = getParameter("Please enter temperature in celcious: ");
  std::cout << "Using parameters: distance " << result[0] << " NM, weight "
            << result[1] << " lbs., height " << result[2]
            << " feet, and temperature " << result[3] << " celcious."
            << "\n";
  return result;
}

// Return list of possible values for key in the dictionaries in dictionaryList
std::vector<double> getDictValues(std::vector<json> dictionaryList, std::string key) {
  std::vector<double> result;
  for (json dict : dictionaryList) {
    result.push_back(dict[key]);
  }
  return result;
}

// From a list of dictionaries, return the dictionary with the key-value closest
// to target_value. Note that we need to check all, since the list might not be
// sorted.
json getClosestdict(std::vector<json> dictionaryList, std::string key,
                    double target_value) {
  double minDist = abs(target_value - dictionaryList[0][key].get<double>());
  json result = dictionaryList[0];
  for (json dict : dictionaryList) {
    if (abs(dict[key].get<double>() - target_value) < minDist) {
      minDist = abs(dict[key].get<double>() - target_value);
      result = dict;
    }
  }
  return result;
}

// Return flight time and fuel use for a single flight, found in dataFile
// according to parameters.
std::array<double, 2> getSingleFlightInfo(std::string dataFile,
                                     std::array<double, 4> parameters) {
  // Open JSON file
  std::ifstream f(dataFile);
  json tmpDict = json::parse(f);

  // Find relevant data.
  tmpDict = getClosestdict(tmpDict["cruise"][0]["weights"], "weight_lbs", parameters[1]);
  tmpDict = getClosestdict(tmpDict["temperatures"], "disa_c", parameters[4]);
  tmpDict = getClosestdict(tmpDict["cruisePoints"], "altitude_ft", parameters[3]);
  double speed = tmpDict["speed_ktas"];
  double fuelFlow = tmpDict["fuelFlow_pph"];

  // Calculate flight time and fuel use.
  std::array<double, 2> result;
  result[0] = parameters[0] / speed;
  result[1] = result[0] * fuelFlow;

  return result;
}

// Requesting user provides the parameters.
void mainTask() {
  // Load parameters to look up
  std::array<double, 4> parameters = getParameters();
  // Get info for flight
  std::array<double, 2> timeAndFuel =
      getSingleFlightInfo("Cirrus.json", parameters);
  // Not sure if this is the best way to convert to time format, but whatever.
  // Note that it always rounds down.
  std::cout << "Flight time is " << (int)timeAndFuel[0] << ":"
            << ((int)(timeAndFuel[0] * 60)) % 60 << " hours and fuel use is "
            << timeAndFuel[1] << " lbs." << "\n";
}

// with parameters provided {distance, weight, height, temperature}.
void mainTask(std::array<double, 4> parameters) {
  // Get info for flight
  std::array<double, 2> timeAndFuel = getSingleFlightInfo("Cirrus.json", parameters);
  std::cout << "Flight time is " << (int)timeAndFuel[0] << ":"
            << ((int)(timeAndFuel[0] * 60)) % 60 << " hours and fuel use is "
            << timeAndFuel[1] << " lbs." << "\n";
}

// Solution for additional challenge.
void optionalChallenge(std::string dataFile, double distance, std::vector<double> weights,
                       std::vector<double> temperatures) {
  for (double weight : weights) {
    for (double temperature : temperatures) {
      // To avoid repeating the repeat calls in each loop, we could instead
      // rename tmpDict for each level. This would be a tradeoff where we
      // instead use more memory.
      std::ifstream f(dataFile);
      json tmpDict = json::parse(f);
      tmpDict = getClosestdict(tmpDict["cruise"][0]["weights"], "weight_lbs", weight);
      tmpDict = getClosestdict(tmpDict["temperatures"], "disa_c", temperature);

      // Retrieve known altitude options for this weight/temperature.
      std::vector<double> altitudes =
          getDictValues(tmpDict["cruisePoints"], "altitude_ft");

      // Use the first altitude option to find starting values.
      std::array<double, 2> timeAndFuel = getSingleFlightInfo(
          dataFile, {distance, weight, altitudes[0], temperature});
      double minTime = timeAndFuel[0], minFuel = timeAndFuel[1],
             minTimeAlt = altitudes[0], minFuelAlt = altitudes[0];

      // Check if any other altitude option is faster/more fuel efficient.
      for (json dict : tmpDict["cruisePoints"]) {
        std::array<double, 2> timeAndFuel = getSingleFlightInfo(
            dataFile,
            {distance, weight, dict["altitude_ft"], temperature});
        if (timeAndFuel[0] < minTime) {
	  minTimeAlt = dict["altitude_ft"];
        }
        if (timeAndFuel[1] < minFuel) {
	  minFuelAlt = dict["altitude_ft"];
        }
      }

      // Print fastest and most fuel efficient option.
      std::cout << "Weight: " << weight << " lbs.; Temperature: " << temperature
                << " celsius.\n    Minimal flight time is " << (int)minTime
                << ":" << ((int)(timeAndFuel[0] * 60)) % 60 << " hours at "
                << minTimeAlt << " feet.\n    Minimal fuel use is " << minFuel
                << " lbs. at " << minFuelAlt << " feet." << "\n";
    }
  }
}

int main() {
  // mainTask();
  optionalChallenge("Cirrus.json", 666.0, {3000, 3800}, {10, -100});
  return 0;
}
