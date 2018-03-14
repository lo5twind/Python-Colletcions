#!/usr/bin/env python
# coding=utf-8

"""
procedure quicksort(a, left, right)
    if right > left
        select a pivot value a[pivotIndex]
        pivotNewIndex := partition(a, left, right, pivotIndex)
        quicksort(a, left, pivotNewIndex-1)
        quicksort(a, pivotNewIndex+1, right)
"""

def swap(a, b):
    pass

def quick_sort(nums, start_idx, end_idx):
    if start_idx >= end_idx:
        return
    s = start_idx
    # select pivot
    pivot_idx = end_idx
    pivot_val = nums[pivot_idx]
    for idx in range(start_idx, end_idx):
        if nums[idx] < pivot_val:
            # swap nums[s] and nums[idx]
            nums[s], nums[idx] = nums[idx], nums[s]
            s += 1
    # swap pivot and current nums[s]
    nums[pivot_idx], nums[s] = nums[s], nums[pivot_idx]

    quick_sort(nums, start_idx, s - 1)
    quick_sort(nums, s + 1, end_idx)


def exchange_sort(nums):
    exchange_len = len(nums)
    while exchange_len > 0:
        # do exchange for nums[0:exchange_len]
        for i in range(exchange_len - 1):
            if nums[i] > nums[i + 1]:
                nums[i], nums[i + 1] = nums[i + 1], nums[i]
        exchange_len -= 1


def exchange_sort_recurse(nums, start_idx, end_idx):
    if start_idx >= end_idx:
        return
    for idx in range(start_idx, end_idx):
        if nums[idx] > nums[idx + 1]:
            nums[idx], nums[idx + 1] = nums[idx + 1], nums[idx]
    exchange_sort_recurse(nums, start_idx, end_idx - 1)


def select_sort(nums):
    pass


if __name__ == "__main__":
    n = [7, 3, 7, 8, 5, 2, 1, 9, 5, 4]
    print n
    quick_sort(n, 0, len(n) - 1)
    print "quick sort result: %s" % n

    n = [7, 3, 7, 8, 5, 2, 1, 9, 5, 4]
    exchange_sort(n)
    print "exchange sort result: %s" % n

    n = [7, 3, 7, 8, 5, 2, 1, 9, 5, 4]
    exchange_sort_recurse(n, 0, len(n) - 1)
    print "exchange sort(recurse) result: %s" % n
