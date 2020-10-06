#ifndef INIREADER_H
#define INIREADER_H

#include <fstream>
#include <iostream>
#include <map>
#include <sstream>
#include <stdexcept>
#include <vector>

#define XTEXT Xtext << classname_ << "::" << __func__ << "()"

/// Class INIreader reads an '.ini' file, and stores
/// ini-data items (unique identifiers and corresponding values) into
/// an internal map (all data in string format).
/// This map can be consulted by client code for initialising var's.
/// The client code is responsible for converting the string format stored
/// in the internal map to the required type by overloading the input
/// stream operator for the corresponding type.
///
/// INIreader is implemented according to the singleton pattern:
/// ctor is protected, a static function #instance() returns a reference
/// to static local #INIreader object. A lot of developers consider singletons
/// bad practice.
///
/// @short A class for '.ini' file reading and 'ini' data handling.
class INIreader
{
   friend std::ostream& operator<<(std::ostream& os,
                                  const INIreader& iniReader);

public:
   /// Returns a reference to a static INIreader object (singleton).
   static INIreader& instance()
   {
     static INIreader iniReader;
     return iniReader;
   }
   INIreader(const INIreader&) = delete;
   INIreader& operator=(const INIreader&) = delete;
   virtual ~INIreader() = default;
   /// Set file name of .ini file.
   /// @param fileName  name of .ini file.
   void setFileName(const std::string& fileName);
   /// Initialising INIreader.
   /// @exception std::runtime_error the .ini file can't be opened.
   void init();
   /// Fill the internal map by an istream input.
   void fillINImap(std::istream& In, const std::string& endINIline);
   /// Add one data item to the internal map
   void addToINImap(const std::string& key, const std::string& value);

   /// Getting the coresponding value for the requested data item.
   /// @param dataName  name of data item
   /// @param pData     pointer to memory address to store an array of type T
   /// @param nData     number of array elements to be stored
   /// @exception std::runtime_error the requested data item is not found.
   /// @exception std::runtime_error the requested data item can't be converted
   /// to type T.
   template<class T>
   void getData(const std::string& dataName, T* pData, const int nData = 1) const
   {
      const auto d = findDataValue(dataName)->second[0];
      std::stringstream ss{d};

      for (int i = 0; i < nData; i++)
      {
         ss >> pData[i];
         /// @todo Check if (buffer.fail() || ((i+1) == nData && !buffer.eof()))
         if (ss.fail())
         {
            std::stringstream Xtext;
            XTEXT << " requested argument format for '"
                  << dataName << "'  #" << nData << " not correct" << std::ends;
            throw std::runtime_error(Xtext.str());
         }
      }
   }

   /// Getting the corresponding s(*iterMap).second.begin();tring for the
   /// requested data item.
   /// @param dataName name of data item
   /// @param data reference to store a string (do not use a pointer)
   /// @exception std::runtime_error the requested data item is not found.
   void getData(const std::string& dataName, std::string& data) const;

   /// Clear internal map.
   void clear();

protected:
   INIreader(const std::string &commentSeparator = "//");

private:
   using INImap_t = std::map<std::string, std::vector<std::string>>;
   using INImap_const_iter_t = INImap_t::const_iterator;

   const std::string classname_;
   const std::string commentSeparator_;
   std::string fileName_;
   std::string line_;
   int lineNumber_;
   /// Internal map <string, vector<string>> for storing unique data item
   /// names and their corresponding values (all in string format).
   INImap_t INImap_;

   void fillINImap(std::ifstream &INIfile);
   /// Removes comment part out of input string.
   void removeComment();
   /// Getting the right hand site string of an assignment statement,
   /// syntax: <LHS> + '=' + <RHS>.
   /// @param RHSline  string containing RHS of the assignment statement.
   /// @exception  a '=' isn't found in line read.
   void getRHSassignment(std::string& RHSline) const;

   /// Gets the left hand site string of an assignment statement,
   /// syntax: <LHS> + '=' + <RHS>.
   /// @param RHSline  string containing LHS of the assignment statement.
   /// @exception  if a '=' isn't found in the line read.
   void getLHSassignment(std::string& LHSline) const;

   /// Checks if line contains a section, syntax:
   /// '[' + <system ID> + ':' + <prefix data name> + ']'.
   /// @pre line contains no leading and trailing spaces and tabs.
   /// @return  true if input string is a section false if not.
   bool lineIsSection() const;

   /// Parse section line and subtract data contents.
   /// @param MustBeAddedToMap indicates if the data item read must be added
   /// to the map.
   /// @param PrefixdataName  string to be add as a prefix to data name
   /// read from the input file.
   void getSectionData(bool& mustBeAddedToMap, std::string& prefixDataName);

   /// Finds data in internal map.
   /// @param dataName string containing name of data item.
   /// @return const_iterator to argument string in the internal map.
   /// @exception std::runtime_error the requested data item is not found
   /// in the internal map.
   INImap_const_iter_t findDataValue(const std::string& dataName) const;
   bool dataNameIsUnique(const std::string& dataName) const;
};

#endif
