import java.util.*;
public class test{
	public int vsort(int[] arr,int left,int right){
			int pivot = arr[left];
			int i = left+1;
			int j = right;
			while(true){
				while(i<=j&&arr[i]<=pivot) i++;
				while(i<=j&&arr[j]>=pivot) j--;
				if (i>j) {
					break;
				}
				int temp = arr[i];
				arr[i] = arr[j];
				arr[j] = temp;
			}
			arr[left] =arr[j];
			arr[j] = pivot;
			return j;
		}
	public void sort(int[] arr,int left,int right){
		int st;
		if (left<right) {
			st = vsort(arr,left,right);
			sort(arr,left,st-1);
			sort(arr,st+1,right);
		}
	}
	public static void main(String[] args) {
	int[] arr ={546,41,888,451,66521,2};
	test t =new test();
	t.sort(arr,0,arr.length-1);
	System.out.println(Arrays.toString(arr));
	}
}
