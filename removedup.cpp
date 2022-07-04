#include <iostream>
#include <vector>
using namespace std;
class Solution {
public:
    int removeDuplicates(vector<int>& nums) {
        vector<int>::iterator it;
        int prod=nums[0];
        for (it=nums.begin();it!=nums.end();it++) {
            cout<<*it<<" ";
        }
        
        return 0;
    }
};
int main() {
    vector<int> nums = {1,1,2};
    Solution().removeDuplicates(nums);
    return 0;
}