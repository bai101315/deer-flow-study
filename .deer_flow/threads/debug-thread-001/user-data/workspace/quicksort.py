"""
快速排序算法 (Quick Sort)
时间复杂度: 平均 O(n log n), 最坏 O(n²)
空间复杂度: O(log n)
稳定排序: 否
"""


def quicksort(arr):
    """
    快速排序主函数
    
    Args:
        arr: 待排序的列表
    
    Returns:
        排序后的列表
    """
    if len(arr) <= 1:
        return arr
    
    # 选择基准元素 (这里使用最后一个元素)
    pivot = arr[-1]
    
    # 分区：小于基准的元素在左边，大于基准的元素在右边
    left = [x for x in arr[:-1] if x < pivot]
    right = [x for x in arr[:-1] if x >= pivot]
    
    # 递归排序左右两部分，然后合并
    return quicksort(left) + [pivot] + quicksort(right)


def quicksort_inplace(arr, low=0, high=None):
    """
    原地快速排序 (节省空间)
    
    Args:
        arr: 待排序的列表
        low: 起始索引
        high: 结束索引
    """
    if high is None:
        high = len(arr) - 1
    
    if low < high:
        # 分区操作，返回基准元素的正确位置
        pivot_idx = partition(arr, low, high)
        
        # 递归排序基准元素左右两边
        quicksort_inplace(arr, low, pivot_idx - 1)
        quicksort_inplace(arr, pivot_idx + 1, high)
    
    return arr


def partition(arr, low, high):
    """
    分区操作
    
    Args:
        arr: 列表
        low: 起始索引
        high: 结束索引
    
    Returns:
        基准元素的最终位置
    """
    pivot = arr[high]  # 选择最后一个元素作为基准
    i = low - 1  # 小于基准的元素的最后位置
    
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    # 将基准元素放到正确位置
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


# 测试代码
if __name__ == "__main__":
    # 测试用例
    test_cases = [
        [64, 34, 25, 12, 22, 11, 90],
        [5, 2, 9, 1, 7, 6, 3],
        [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5],
        [1],
        [],
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],
    ]
    
    print("快速排序算法测试\n" + "=" * 40)
    
    for i, arr in enumerate(test_cases):
        original = arr.copy()
        sorted_arr = quicksort(arr.copy())
        print(f"\n测试 {i + 1}:")
        print(f"  输入: {original}")
        print(f"  输出: {sorted_arr}")
    
    print("\n" + "=" * 40)
    print("原地快速排序测试:\n")
    
    for i, arr in enumerate(test_cases):
        original = arr.copy()
        quicksort_inplace(arr)
        print(f"测试 {i + 1}: {original} -> {arr}")