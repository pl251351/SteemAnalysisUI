from scipy.stats import pearsonr

from steemanalysis.database_repo import DataRepository

repo = DataRepository('../instance/repo.db')


def print_data(df, name):
    df_compound_positive = df[df[name] > 0.25]
    df_compound_positive = df_compound_positive[
        df_compound_positive[name] > df_compound_positive[name].quantile(.05)]
    df_compound_positive = df_compound_positive[
        df_compound_positive[name] < df_compound_positive[name].quantile(.9995)]
    df_compound_negative = df[df[name] < -0.25]
    df_compound_negative = df_compound_negative[
        df_compound_negative[name] > df_compound_negative[name].quantile(.05)]
    df_compound_negative = df_compound_negative[
        df_compound_negative[name] < df_compound_negative[name].quantile(.9995)]
    print("-" * 50)
    print(df_compound_negative.corr(method="spearman"))
    pr = pearsonr(df_compound_negative[name], df_compound_negative['value_earned'])
    print("-" * 50)
    print(df_compound_negative.describe())
    print("-" * 50)
    print("pearson correlation negative")
    print(pr)
    print("-" * 50)
    print("-" * 50)
    print(df_compound_positive.corr(method="spearman"))
    pr = pearsonr(df_compound_positive[name], df_compound_positive['value_earned'])
    print("-" * 50)
    print(df_compound_positive.describe())
    print("-" * 50)
    print("pearson correlation positive")
    print(pr)
    print("-" * 50)


# df = repo.select_for_vader_correlation_analysis()
# print_data(df)
# print("-" * 50)
# print("Google analysis")
df = repo.select_for_combined_correlation_analysis()
# df['compound'] = df['vader']
del df["google"]
del df["ibm"]
print_data(df, 'vader')
print("-" * 50)
print("Google analysis")
print("-" * 50)
df = repo.select_for_combined_correlation_analysis()
# df['compound'] = df['google']
del df["vader"]
del df["ibm"]
print_data(df, 'google')
print("-" * 50)
print("IBM analysis")
print("-" * 50)
df = repo.select_for_combined_correlation_analysis()
# df['compound'] = df['google']
del df["google"]
del df["vader"]
print_data(df, 'ibm')


# corr = df.corr()
#
# print("-"*50)
# print("Correlation")
# print("pos-%d neg-%d neu-%d" %(len(df["pos"]), len(df["neg"]), len(df["neu"])))
# print(corr)
# print("-"*50)
#
# pr = pearsonr(df['neg'], df['value_earned'])
# print("-"*50)
# print("pearson correlation negative")
# print(pr)
# print("-"*50)
#
# pr = pearsonr(df['neu'], df['value_earned'])
# print("-"*50)
# print("pearson correlation neutral")
# print(pr)
# print("-"*50)
#
# pr = pearsonr(df['pos'], df['value_earned'])
# print("-"*50)
# print("pearson correlation positive")
# print(pr)
# print("-"*50)

# df_neg = df[['neg', 'value_earned']]
# df_neg_fil = df_neg[(df_neg['neg'] != 0) & (df_neg['value_earned'] != 0)]
# print("-"*50)
# print("correlation with zero value rows removed - negative")
# print(df_neg_fil.describe())
# print(df_neg_fil.corr())
# print("-"*50)
#
# df_pos = df[['pos', 'value_earned']]
# df_pos_fil = df_pos[(df_pos['pos'] != 0) & (df_pos['value_earned'] != 0)]
# print("-"*50)
# print("correlation with zero value rows removed - positive")
# print(df_pos_fil.describe())
# print(df_pos_fil.corr())
# print("-"*50)
#
# df_neu = df[['neu', 'value_earned']]
# df_neu_fil = df_neu[(df_neu['neu'] != 0) & (df_neu['value_earned'] != 0)]
# print("-"*50)
# print("correlation with zero value rows removed - neutral")
# print(df_neu_fil.describe())
# print(df_neu_fil.corr())
# print("-"*50)
#
# pr = pearsonr(df_neu_fil['neu'], df_neu_fil['value_earned'])
# print("-"*50)
# print("pearson correlation with zero value rows removed - neutral")
# print(pr)
#
# pr = pearsonr(df_neg_fil['neg'], df_neg_fil['value_earned'])
# print("-"*50)
# print("pearson correlation with zero value rows removed - negative")
# print(pr)
#
# pr = pearsonr(df_pos_fil['pos'], df_pos_fil['value_earned'])
# print("-"*50)
# print("pearson correlation with zero value rows removed - positive")
# print(pr)
