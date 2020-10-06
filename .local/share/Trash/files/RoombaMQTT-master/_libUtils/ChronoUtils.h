#include <chrono>
#include <type_traits>

template <typename T>
struct is_chrono_duration : std::false_type {
};

template <typename Rep, typename Period>
struct is_chrono_duration<std::chrono::duration<Rep, Period>> : std::true_type {
};

template <typename T>
constexpr bool is_chrono_duration_v = is_chrono_duration<T>::value;
