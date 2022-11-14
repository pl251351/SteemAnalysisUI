from scipy.stats import pearsonr


def _to_html(pr):
    html = f'''
    <table border="1" class="dataframe">
        <thead>
            <tr style="text-align: right;">
                <th>Statistic</th>
                <th>pvalue</ht>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>{pr.statistic}</td>
                <td>{pr.pvalue}</td>
            </tr>
        </tbody>
    </table>
    '''

    return html


def analyze(df, name, start=0.0, drop_bottom=.05, drop_top=.9995, drop_zero=False):
    df_non_zero = df
    if drop_zero:
        df_non_zero = df[df['value_earned'] > 0]

    # where does positive and negative start
    df_compound_positive = df_non_zero[df_non_zero[name] > start]

    # drop bottom most values
    if drop_bottom > 0:
        bottom_quantile = df_compound_positive[name].quantile(drop_bottom)
        df_compound_positive = df_compound_positive[df_compound_positive[name] > bottom_quantile]
    # drop top most values
    if drop_top < 1:
        top_quantile = df_compound_positive[name].quantile(drop_top)
        df_compound_positive = df_compound_positive[df_compound_positive[name] < top_quantile]

    # where does negative start
    df_compound_negative = df_non_zero[df_non_zero[name] < -1 * start]
    # make negative values positive
    df_compound_negative[name] = df_compound_negative[name].abs()


    # drop bottom most values
    if drop_bottom > 0:
        bottom_quantile = df_compound_negative[name].quantile(drop_bottom)
        df_compound_negative = df_compound_negative[df_compound_negative[name] > bottom_quantile]
    # drop bottom most values
    if drop_top < 1:
        top_quantile = df_compound_negative[name].quantile(drop_top)
        df_compound_negative = df_compound_negative[df_compound_negative[name] < top_quantile]

    # calculate stat for negative

    # spearman correlation
    spearman_df = df_compound_negative.corr(method="spearman")
    spearman_neg = spearman_df.to_html()

    # pearson co-relation with p-value
    pr = pearsonr(df_compound_negative[name], df_compound_negative['value_earned'])
    pearson_neg = _to_html(pr)

    # descriptive statistics
    negative_desc = df_compound_negative.describe().to_html()

    # calculate stat for positive

    # spearman correlation
    spearman_df = df_compound_positive.corr(method="spearman")
    spearman_pos = spearman_df.to_html()

    # pearson co-relation with p-value
    pr = pearsonr(df_compound_positive[name], df_compound_positive['value_earned'])
    pearson_pos = _to_html(pr)

    # descriptive statistics
    positive_desc = df_compound_positive.describe().to_html()

    return negative_desc, spearman_neg, pearson_neg, positive_desc, spearman_pos, pearson_pos
