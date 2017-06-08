# Copyright (c) 2017, All Contributors (see CONTRIBUTORS file)
# Authors: Cristina Muntean <cristina.muntean@isti.cnr.it>
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

"""
import numpy as np
from abc import ABCMeta, abstractmethod
import six


class Metric(six.with_metaclass(ABCMeta)):
    """
    Metric is an abstract class which provides an interface for specific metrics.
    It also offers 2 methods, one for iterating over the indeces for a certain query 
    and another for iterating over the entire dataset based on those indeces. 
    """

    @abstractmethod
    def __init__(self, name):
        """
        The constructor for any metric; it initializes that metric with the proper name.
        
        Parameters
        ----------
        name : string
            Represents the name of that metric instance.
        """
        self.name = name

    @abstractmethod
    def eval(self, dataset, y_pred):
        """
        This abstract method computes a specific metric over the predicted scores for a test dataset

        Parameters
        ----------
        dataset
        y_pred

        Returns
        -------

        """
        self.detailed_scores = np.zeros(dataset.n_queries, dtype=np.float32)

    @abstractmethod
    def eval_per_query(self, y, y_pred):
        """

        This abstract methods helps to evaluate the predicted scores for a specific query within the dataset.

        Parameters
        ----------
        y
        y_pred

        Returns
        -------

        """

    def query_indeces(self, dataset, y_pred):
        """
        This method implements and iterator of the query_ids in the dataset.

        Parameters
        ----------
        dataset : Dataset
        y_pred : numpy.array

        Returns
        -------
        numpy.ndarray
            The row index of instances belonging to the same query.

        """
        assert len(y_pred) == len(dataset.y)
        for i in np.arange(len(dataset.query_ids)-1):
            yield np.arange(dataset.query_ids[i], dataset.query_ids[i+1])


    def query_iterator(self, dataset, y_pred):
        """
        This method iterates over dataset document scores and predicted scores in blocks of instances
        which belong to the same query.
        Parameters
        ----------
        dataset :  Datatset
        y_pred  : numpy.array

        Returns
        -------
        int:
            The query id.
        numpy.array:
            The document scores of the instances in the labeled dataset (instance labels) belonging to the same query id.
        numpy.array:
            The predicted scores for the instances in the dataset belonging to the same query id.
        """
        for query_id, query_line_indeces in enumerate(self.query_indeces(dataset, y_pred)):
            yield query_id, dataset.y[query_line_indeces], y_pred[query_line_indeces]