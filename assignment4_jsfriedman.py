# Jonathan Friedman
# CS 5007
# Time for completion: approximately 11 hours. I seriously did not understand PANDAS when starting this assignment

import sys
import copy
import numpy as np
import pandas as pd
from scipy import stats

# types are inferred correctly when reading in the data
# 0 = problem set id : int
# 2 = user id : int
# 3 = condition : string
# 30 = complete : int
# 31 = problem count : int
KEEP_LIST_INDEX = [0, 2, 3, 30, 31]

SUMMARY_STATISTICS_LABELS = []
SUMMARY_STATISTICS_LABELS.append("problem_set")
SUMMARY_STATISTICS_LABELS.append("condition")
SUMMARY_STATISTICS_LABELS.append("number_of_students")
SUMMARY_STATISTICS_LABELS.append("total_problems")
SUMMARY_STATISTICS_LABELS.append("problems_per_student_mean")
SUMMARY_STATISTICS_LABELS.append("problems_per_student_sd")
SUMMARY_STATISTICS_LABELS.append("completion_count")
SUMMARY_STATISTICS_LABELS.append("completion_percent_mean")
SUMMARY_STATISTICS_LABELS.append("completion_percent_sd")
SUMMARY_STATISTICS_LABELS.append("log_problem_count_mean")
SUMMARY_STATISTICS_LABELS.append("log_problem_count_sd")

CHI_SQUARED_LABELS = []
CHI_SQUARED_LABELS.append("problem_set")
CHI_SQUARED_LABELS.append("control_n")
CHI_SQUARED_LABELS.append("experiment_n")
CHI_SQUARED_LABELS.append("control_mean")
CHI_SQUARED_LABELS.append("experiment_mean")
CHI_SQUARED_LABELS.append("df")
CHI_SQUARED_LABELS.append("chi_squared_statistic")
CHI_SQUARED_LABELS.append("p_value")

TTEST_LABELS = []
TTEST_LABELS.append("problem_set")
TTEST_LABELS.append("control_n")
TTEST_LABELS.append("experiment_n")
TTEST_LABELS.append("control_mean")
TTEST_LABELS.append("experiment_mean")
TTEST_LABELS.append("df")
TTEST_LABELS.append("t_statistic")
TTEST_LABELS.append("p_value")


class Assignment4:
    def __init__(self):
        """
        Initializes self.__original_data to None
        Initializes self.__preprocessed_data to None
        Initializes self.__summary_statistics_data to None
        Initializes self.__ttest_data to None
        Initializes self.__chi_squared_data to None
        """

        self.__original_data = None
        self.__preprocessed_data = None
        self.__summary_statistics_data = None
        self.__chi_squared_data = None
        self.__ttest_data = None

    @property
    def original_data(self):
        return self.__original_data

    @original_data.setter
    def original_data(self, original_data):
        self.__original_data = original_data

    @property
    def preprocessed_data(self):
        return self.__preprocessed_data

    @preprocessed_data.setter
    def preprocessed_data(self, preprocessed_data):
        self.__preprocessed_data = preprocessed_data

    @property
    def summary_statistics(self):
        return self.__summary_statistics_data

    @summary_statistics.setter
    def summary_statistics(self, summary_statistics):
        self.__summary_statistics_data = summary_statistics

    @property
    def chi_squared_data(self):
        return self.__chi_squared_data

    @chi_squared_data.setter
    def chi_squared_data(self, chi_squared_data):
        self.__chi_squared_data = chi_squared_data

    @property
    def ttest_data(self):
        return self.__ttest_data

    @ttest_data.setter
    def ttest_data(self, ttest_data):
        self.__ttest_data = ttest_data

    def read_data(self, file_path):

        self.__original_data = pd.read_csv(file_path)

    def preprocess(self):

        self.__preprocessed_data = self.__original_data
        self.__drop_columns()
        self.__fix_column_names()
        self.__add_log_problem_count()

    def __drop_columns(self):

        cols = []
        for n in range(32):
            if n not in KEEP_LIST_INDEX:
                cols.append(n)

        self.__preprocessed_data.drop(self.__preprocessed_data.columns[cols], axis=1, inplace=True)


    def __fix_column_names(self):

        self.__preprocessed_data.rename(columns={'User ID': 'user_id', 'Condition': 'condition', 'Problem Count': 'problem_count'}, inplace=True)

    def __add_log_problem_count(self):

        self.__preprocessed_data['log_count'] = np.NaN
        self.__preprocessed_data['log_count'] = np.log10(self.__preprocessed_data.loc[self.__preprocessed_data['complete'] == 1]['problem_count'])

    def calculate_summary_statistics(self):

        column_titles = ['problem_set', 'condition', 'number_of_students','total_problems',	'problems_per_student_mean',	'problems_per_student_sd',	'completion_count',	'completion_percent_mean',	'completion_percent_sd',	'log_problem_count_mean',	'log_problem_count_sd']
        self.__summary_statistics_data = pd.DataFrame(columns = column_titles)

        unique_problem_sets = self.__preprocessed_data.problem_set.unique()
        conditions = self.__preprocessed_data.condition.unique()
        for problem_set in unique_problem_sets:
            one_condition = self.__preprocessed_data.loc[self.__preprocessed_data['problem_set'] == problem_set]
            vars = pd.Series()
            number_of_students = one_condition['user_id'].nunique()
            total_problems = one_condition['problem_count'].sum()
            problems_per_student_mean = np.mean(one_condition['problem_count'])
            problems_per_student_sd = np.std(one_condition['problem_count'])
            completed = one_condition.loc[one_condition['complete'] == 1]['complete'].sum()
            completed_percent = one_condition['complete'].mean()
            completed_percent_std = np.std(one_condition['complete'])
            log_problem_count_mean = np.mean(one_condition.loc[one_condition['complete'] == 1]['log_count'])
            log_problem_count_sd = np.std(one_condition.loc[one_condition['complete'] == 1]['log_count'])
            vars['problem_set'] = problem_set
            vars['condition'] = 'ALL'
            vars['number_of_students'] = number_of_students
            vars['total_problems'] = total_problems
            vars['problems_per_student_mean'] = problems_per_student_mean
            vars['problems_per_student_sd'] = problems_per_student_sd
            vars['completion_count'] = completed
            vars['completion_percent_mean'] = completed_percent
            vars['completion_percent_sd'] = completed_percent_std
            vars['log_problem_count_mean'] = log_problem_count_mean
            vars['log_problem_count_sd'] = log_problem_count_sd
            self.__summary_statistics_data = self.__summary_statistics_data.append(vars,ignore_index=True)

            for cond in conditions:
                two_condition = one_condition.loc[one_condition['condition'] == cond]
                number_of_students = two_condition['user_id'].nunique()
                total_problems = two_condition['problem_count'].sum()
                problems_per_student_mean = np.mean(two_condition['problem_count'])
                problems_per_student_sd = np.std(two_condition['problem_count'])
                completed = two_condition.loc[two_condition['complete'] == 1]['complete'].sum()
                completed_percent = two_condition['complete'].mean()
                completed_percent_std = np.std(two_condition['complete'])
                log_problem_count_mean = np.mean(two_condition.loc[two_condition['complete'] == 1]['log_count'])
                log_problem_count_sd = np.std(two_condition.loc[two_condition['complete'] == 1]['log_count'])
                vars['problem_set'] = problem_set
                vars['condition'] = cond
                vars['number_of_students'] = number_of_students
                vars['total_problems'] = total_problems
                vars['problems_per_student_mean'] = problems_per_student_mean
                vars['problems_per_student_sd'] = problems_per_student_sd
                vars['completion_count'] = completed
                vars['completion_percent_mean'] = completed_percent
                vars['completion_percent_sd'] = completed_percent_std
                vars['log_problem_count_mean'] = log_problem_count_mean
                vars['log_problem_count_sd'] = log_problem_count_sd
                self.__summary_statistics_data = self.__summary_statistics_data.append(vars, ignore_index=True)

    def calculate_chi_squared(self):
        """
        Performs a chi-squared test of independence on completion rates between control/experiment groups for all problem sets
        Stores the results in self.__chi_squared_data
        :return:  No return value
        """

        pass
        

    def calculate_ttest(self):
        """
        Performs a t-test of log(problem_count) between control/experiment groups for all problem sets
        Stores the results in self.__ttest_data
        :return:  No return value
        """
        self.__ttest_data = pd.DataFrame(columns= TTEST_LABELS)
        unique_problem_sets = self.__preprocessed_data.problem_set.unique()
        for problem_set in unique_problem_sets:
            filtered = self.__preprocessed_data.loc[self.__preprocessed_data['problem_set'] == problem_set]
            control = filtered[filtered['condition'] == 'C']['log_count']
            experiment = filtered[filtered['condition'] == 'E']['log_count']
            tvars = pd.Series()
            tvars['problem_set'] = problem_set
            tvars['control_n'] = control.count()
            tvars['experiment_n'] = experiment.count()
            tvars['control_mean'] = np.mean(control)
            tvars['experiment_mean'] = np.mean(experiment)
            tvars['df'] = tvars['control_n'] + tvars['experiment_n'] - 2

            result = stats.ttest_ind(control, experiment, equal_var=False, nan_policy="omit")
            tvars['t_statistic'] = result[0]
            tvars['p_value'] = result[1]
            self.__ttest_data = self.__ttest_data.append(tvars, ignore_index= True)



    def output_data_files(self):

        self.__preprocessed_data.to_csv('preprocessed_data2.csv', index=False)
        self.__summary_statistics_data.to_csv('summary_statistics2.csv', index=False)
        #self.__chi_squared_data.to_csv('chi_squared2.csv', index=False)
        self.__ttest_data.to_csv('ttest2.csv', index = False)


if __name__ == "__main__":

    if len(sys.argv) > 1:
        file_path = sys.argv[1]

        assignment4 = Assignment4()
        assignment4.read_data(file_path)
        assignment4.preprocess()
        assignment4.calculate_summary_statistics()
        assignment4.calculate_chi_squared()
        assignment4.calculate_ttest()
        assignment4.output_data_files()

        # Get the input file path from the program arguments
        # If no path was specified do not do any of the following steps

        # Create an Assignment4 object

        # read in data using the read_data method of the Assignment4 object

        # pre-process the data using the preprocess function

        # calculate
        # for each experiment and for each condition
        #   number of students
        #   total problem count
        #   average problems per student
        #   standard deviation problem per student
        #   completion count
        #   completion percent
        #   standard deviation completion percent
        #   average log of problem count
        #   standard deviation of log of problem count

        # for each experiment
        # run chi-squared test of independence for completion rate
        # run t-test on log problem count

        # output results

    else:
        print("Enter an input file path for program arguments\n")