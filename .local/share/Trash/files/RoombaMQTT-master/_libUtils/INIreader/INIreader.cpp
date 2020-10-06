#include <fstream>
#include <iostream>
#include <stdexcept>
#include "INIreader.h"
#include "stringExt.h"

namespace
{
/// String format ".....", double quoted string.
/// @pre no leading and trailing spaces or tabs.
void processEscChars(std::string& str)
{
   if (str.size() > 1
       and str[0] == '"'
       and str[str.size() - 1] == '"')
   {
      // Remove leading and trailing "
      str.erase(0, 1);
      str.erase(str.size() - 1, 1);
      // Process escape chars
      size_t Index = 0;
      while (Index < str.size() - 1)
      {
         // Check for escape char
         if (str[Index] == '\\')
         {
            switch (str[Index + 1])
            {
            case '\\':
               str[Index] = '\\';
               str.erase(Index + 1, 1);
               break;
            case '"':
               str[Index] = '"';
               str.erase(Index + 1, 1);
               break;
            case 'n':
               str[Index] = '\n';
               str.erase(Index + 1, 1);
               break;
            case 't':
               str[Index] = '\t';
               str.erase(Index + 1, 1);
               break;
            default:
               // Remove '\' char
               str.erase(Index, 1);
               break;
            }
         }
         ++Index;
      }
   }
}
}

std::ostream& operator<<(std::ostream& os, const INIreader& iniReader)
{
   for (auto& mappedData: iniReader.INImap_)
   {
      for (auto& str: mappedData.second)
      {
         os << mappedData.first << " = " << str << std::endl;
      }
   }

   return os;
}

void INIreader::setFileName(const std::string& fileName)
{
   fileName_ = fileName;
   init();
}

void INIreader::init()
{
   std::ifstream INIfile;

   INIfile.open(fileName_.c_str());
   if (not INIfile.good())
   {
      std::ostringstream Xtext;
      XTEXT << " can't open file '" << fileName_ << "'" << std::ends;
      throw std::runtime_error(Xtext.str());
   }
   fillINImap(INIfile);
   INIfile.close();
}

void INIreader::getData(const std::string& dataName, std::string& data) const
{
   data = (*findDataValue(dataName)).second[0];
   processEscChars(data);
}

void INIreader::clear()
{
   INImap_.clear();
}

void INIreader::fillINImap(std::istream& InputStream,
                           const std::string& EndINIline)
{
   std::string RHSline;
   std::vector<std::string> RHSlines;
   std::string LHSline;
   std::string PreviousLHSline;
   bool mustBeAddedToMap{true};
   std::string PrefixdataName;
   bool INIisEnded{false};

   while (not InputStream.eof() and not INIisEnded)
   {
      // read line by line
      getline(InputStream, line_);
      ++lineNumber_;
      // if DOS format: remove \r
      utils::removeReturns(line_);
      removeComment();
      utils::removeLeadingTrailingSpacesTabs(line_);
      if (not line_.empty())
      {
         INIisEnded = (line_ == EndINIline);
         if (not INIisEnded and lineIsSection())
         {
            getSectionData(mustBeAddedToMap, PrefixdataName);
            PreviousLHSline = "";
         }
         else
         {
            if (not INIisEnded and mustBeAddedToMap)
            {
               getRHSassignment(RHSline);
               utils::replaceCommasBySpaces(RHSline);
               getLHSassignment(LHSline);
               if (LHSline.empty())
               {
                  LHSline = PreviousLHSline;
                  RHSlines.push_back(RHSline);
               }
               else
               {
                  PreviousLHSline = LHSline;
                  RHSlines.clear();
                  RHSlines.push_back(RHSline);
               }
               if (not PrefixdataName.empty())
               {
                  LHSline = PrefixdataName + "." + LHSline;
               }
               INImap_[LHSline] = RHSlines;
            }
         }
      }
   }
}

void INIreader::addToINImap(const std::string& key, const std::string& value)
{
   std::vector<std::string> values;
   values.push_back(value);
   INImap_[key] = values;
}

//-------------------------------------------------------------------- protected

INIreader::INIreader(const std::string &commentSeparator)
   : classname_{__func__}
   , commentSeparator_{commentSeparator}
   , fileName_{""}
   , line_{""}
   , lineNumber_{0}
   , INImap_{}
{}

//---------------------------------------------------------------------- private

void INIreader::fillINImap(std::ifstream &INIfile)
{
   std::string RHSline;
   std::vector<std::string> RHSlines;
   std::string LHSline;
   std::string PreviousLHSline;
   bool mustBeAddedToMap{true};
   std::string PrefixdataName;

   while (not INIfile.eof())
   {
      // read line by line
      getline(INIfile, line_);
      ++lineNumber_;
      // if DOS format: remove \r
      utils::removeReturns(line_);
      removeComment();
      utils::removeLeadingTrailingSpacesTabs(line_);
      if (not line_.empty())
      {
         if (lineIsSection())
         {
            getSectionData(mustBeAddedToMap, PrefixdataName);
            PreviousLHSline = "";
         }
         else
         {
            if (mustBeAddedToMap)
            {
               getRHSassignment(RHSline);
               utils::replaceCommasBySpaces(RHSline);
               getLHSassignment(LHSline);
               if (LHSline.empty())
               {
                  LHSline = PreviousLHSline;
                  RHSlines.push_back(RHSline);
               }
               else
               {
                  PreviousLHSline = LHSline;
                  RHSlines.clear();
                  RHSlines.push_back(RHSline);
               }
               if (not PrefixdataName.empty())
               {
                  LHSline = PrefixdataName + "." + LHSline;
               }
               INImap_[LHSline] = RHSlines;
            }
         }
      }
   }
}

void INIreader::getRHSassignment(std::string& RHSline) const
{
   size_t pos{line_.find("=")};
   if (pos == std::string::npos)
   {
      std::ostringstream Xtext;
      XTEXT << " syntax error in line " << lineNumber_
            << ": '" << line_ << "', could not find =" << std::ends;
      throw std::runtime_error(Xtext.str());
   }
   RHSline = line_;
   RHSline.erase(0, pos + 1);
   utils::removeLeadingTrailingSpacesTabs(RHSline);
}

void INIreader::getLHSassignment(std::string& LHSline) const
{
   size_t pos{line_.find("=")};
   if (pos == std::string::npos)
   {
      std::ostringstream Xtext;
      XTEXT << " syntax error in line " << lineNumber_
            << ": '" << line_ << "', could not find =" << std::ends;
      throw std::runtime_error(Xtext.str());
   }
   LHSline = line_;
   LHSline.erase(pos);
   utils::removeLeadingTrailingSpacesTabs(LHSline);
}

void INIreader::removeComment()
{
   size_t pos{line_.find(commentSeparator_)};
   if (pos != std::string::npos)
   {
      line_.erase(pos);
   }
}

bool INIreader::lineIsSection() const
{
   return (line_[0] == '[' && line_[line_.size() - 1] == ']');
}

void INIreader::getSectionData(bool& mustBeAddedToMap,
                               std::string& prefixDataName)
{
   // line must be a section
   std::string buffer{line_};
   // remove '[' and ']'
   buffer.erase(0, 1);
   buffer.erase(buffer.size() - 1, 1);
   utils::removeLeadingTrailingSpacesTabs(buffer);
   // create IDline
   std::string IDline{buffer};
   //size_t pos = Buffer.find(':');
   //IDline.assign(Buffer, 0, pos);
   utils::removeLeadingTrailingSpacesTabs(IDline);

   mustBeAddedToMap = false;
   std::istringstream IDBuffer(IDline.c_str());
   std::string ID;
   while (not IDBuffer.fail() and not mustBeAddedToMap)
   {
      IDBuffer >> ID;
      // m_ID = ID;
      //mustBeAddedToMap = (ID == m_ID);
      mustBeAddedToMap = true;
   }
   if (mustBeAddedToMap)
   {
      // create prefixdataName
      prefixDataName.assign(buffer, 0, buffer.size());
      // utils::removeLeadingTrailingSpacesTabs(PrefixdataName);
   }
   else
   {
      prefixDataName.clear();
   }
}

INIreader::INImap_const_iter_t
   INIreader::findDataValue(const std::string& dataName) const
{
   auto iter = INImap_.find(dataName);
   if (iter == end(INImap_))
   {
      std::ostringstream Xtext;
      XTEXT << " could not find '" << dataName << "'" << std::ends;
      throw std::runtime_error(Xtext.str());
   }
   return iter;
}

bool INIreader::dataNameIsUnique(const std::string& dataName) const
{
   return INImap_.find(dataName) == end(INImap_);
}
