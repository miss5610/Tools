class Solution :
    def twoSum(self,nums,target):
        num_map = {}
        for i,num in enumerate(nums):
            complete = target - num
            if complete in num_map:
                return (num_map[complete],i)
            num_map[num] = i
        return []
    
solution = Solution()
a = [15,7,4,9]
b = 19
c = solution.twoSum(a,b)
print(c)

# 練習 git commit