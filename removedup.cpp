#include <iostream>
#include <vector>
using namespace std;
class Solution {
public:
    int removeDuplicates(vector<int>& nums) {
        vector<int>::iterator it;
        int prod=nums[0];
        for (it=++nums.begin();it!=nums.end();it++) {
            if (*it==prod) nums.erase(it);
        }
        
        return nums.size();
    }
};
void output(vector<int>& nums) {
    vector<int>::iterator it;
    for (it=nums.begin();it!=nums.end();it++) {
        cout<<*it<<" ";
    }
    return;
}
int main() {
    vector<int> nums = {1,1,2};
    cout<<Solution().removeDuplicates(nums)<<endl;
    output(nums);
    return 0;
}