#include "stringExt.h"

using namespace std;

void utils::removeLeadingSpacesTabs(string& line)
{
   if (not line.empty())
   {
      while (line[0] == ' '
             or line[0] == '\t')
      {
         line.erase(0, 1);
      }
   }
}

void utils::removeTrailingSpacesTabs(string& line)
{
   if (not line.empty())
   {
      while (line[line.size() - 1] == ' '
             or line[line.size() - 1] == '\t')
      {
         line.erase(line.size() - 1, 1);
      }
   }
}

void utils::removeLeadingTrailingSpacesTabs(string& line)
{
   removeLeadingSpacesTabs(line);
   removeTrailingSpacesTabs(line);
}

void utils::replaceCommasBySpaces(string& line)
{
   size_t pos;
   while ((pos = line.find(string(","))) != string::npos)
   {
      line.replace(pos, 1, " ");
   }
}

void utils::removeReturns(string& line)
{
   size_t pos;
   while ((pos = line.find(string("\r"))) != string::npos)
   {
      line.replace(pos, 1, "");
   }
}

//function to split-up strings, to a vector of strings, using a delimiter
void utils::tokenize(const std::string& str,
                     std::vector<std::string>& tokens,
                     const std::string& delimiters)
{
   // Skip delimiters at beginning.
   auto lastPos = str.find_first_not_of(delimiters, 0);
   // Find first "non-delimiter".
   auto pos = str.find_first_of(delimiters, lastPos);

   while (std::string::npos != pos
          or std::string::npos != lastPos)
   {
      // Found a token, add it to the vector.
      tokens.push_back(str.substr(lastPos, pos - lastPos));
      // Skip delimiters. Note the "not_of"
      lastPos = str.find_first_not_of(delimiters, pos);
      // Find next "non-delimiter"
      pos = str.find_first_of(delimiters, lastPos);
   }
}

void utils::decapitalize(std::string& str)
{
   for (auto &c: str)
   {
      c = tolower(c);
   }
}

void utils::capitalize(std::string& str)
{
   for (auto &c: str)
   {
      c = toupper(c);
   }
}
