#include <iostream>
#include <vector>
using namespace std;

class Solution {
public:
    int removeElement(vector<int>& nums, int val) {
		vector<int>::iterator it;
        for (it=nums.begin();it!=nums.end();) {
            if (*it==val) {nums.erase(it);}
            else it++;
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
    vector<int> nums = {0,1,2,2,3,0,4,2};
	cout<<Solution().removeElement(nums,2)<<endl;
    output(nums);
    return 0;
}