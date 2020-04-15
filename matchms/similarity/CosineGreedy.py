from numpy.matlib import repmat
from numpy import absolute, reshape, zeros_like, where, power, argsort


class CosineGreedy:

    def __init__(self, label, tolerance=0.3):
        self.label = label
        self.tolerance = tolerance

    def __call__(self, spectrum, reference_spectrum):
        def calc_mz_distance():
            mz_row_vector = spectrum.mz
            mz_col_vector = reshape(reference_spectrum.mz, (n_rows, 1))

            mz1 = repmat(mz_row_vector, n_rows, 1)
            mz2 = repmat(mz_col_vector, 1, n_cols)

            return mz1 - mz2

        def calc_intensities_product():
            intensities_row_vector = spectrum.intensities
            intensities_col_vector = reshape(reference_spectrum.intensities, (n_rows, 1))

            intensities1 = repmat(intensities_row_vector, n_rows, 1)
            intensities2 = repmat(intensities_col_vector, 1, n_cols)

            return intensities1 * intensities2

        def calc_intensities_product_within_tolerance():

            mz_distance = calc_mz_distance()
            intensities_product = calc_intensities_product()

            within_tolerance = absolute(mz_distance) <= self.tolerance

            return where(within_tolerance, intensities_product, zeros_like(intensities_product))

        def calc_score():
            r_unordered, c_unordered = intensities_product_within_tolerance.nonzero()
            v_unordered = intensities_product_within_tolerance[r_unordered, c_unordered]
            sortorder = argsort(v_unordered)[::-1]
            r_sorted = r_unordered[sortorder]
            c_sorted = c_unordered[sortorder]

            score = 0
            num_matches = 0
            for r, c in zip(r_sorted, c_sorted):
                if intensities_product_within_tolerance[r, c] > 0:
                    score += intensities_product_within_tolerance[r, c]
                    num_matches += 1
                    intensities_product_within_tolerance[r, :] = 0
                    intensities_product_within_tolerance[:, c] = 0
            return score, num_matches

        n_rows = reference_spectrum.mz.size
        n_cols = spectrum.mz.size

        intensities_product_within_tolerance = calc_intensities_product_within_tolerance()

        squared1 = power(spectrum.intensities, 2)
        squared2 = power(reference_spectrum.intensities, 2)
        score, num_matches = calc_score()
        return score / max(sum(squared1), sum(squared2)), num_matches
